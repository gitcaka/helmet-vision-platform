import threading
import time
from datetime import datetime, timezone

import cv2
import numpy as np


class SharedVideoStream:
    def __init__(
        self,
        url,
        *,
        frame_rate=12,
        jpeg_quality=80,
        open_timeout_ms=3000,
        read_timeout_ms=3000,
        reconnect_initial=0.5,
        reconnect_max=10,
        capture_factory=None,
    ):
        self.url = url
        self.frame_rate = max(1.0, min(float(frame_rate), 60.0))
        self.jpeg_quality = max(30, min(int(jpeg_quality), 95))
        self.open_timeout_ms = max(100, int(open_timeout_ms))
        self.read_timeout_ms = max(100, int(read_timeout_ms))
        self.reconnect_initial = max(0.1, float(reconnect_initial))
        self.reconnect_max = max(self.reconnect_initial, float(reconnect_max))
        self.capture_factory = capture_factory or cv2.VideoCapture

        self._condition = threading.Condition()
        self._stop_event = threading.Event()
        self._thread = None
        self._subscribers = 0
        self._frame_version = 1
        self._latest_frame = self._placeholder("Waiting for RTSP stream")
        self._state = "idle"
        self._last_frame_timestamp = None
        self._last_error = None

    def _placeholder(self, message):
        image = np.full((360, 640, 3), 28, dtype=np.uint8)
        cv2.putText(
            image,
            message,
            (45, 185),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.85,
            (220, 220, 220),
            2,
            cv2.LINE_AA,
        )
        encoded, buffer = cv2.imencode(
            ".jpg",
            image,
            [cv2.IMWRITE_JPEG_QUALITY, self.jpeg_quality],
        )
        return buffer.tobytes() if encoded else None

    def _set_state(self, state, error=None):
        with self._condition:
            self._state = state
            self._last_error = error

    def _publish(self, frame_bytes, *, state="connected", error=None):
        if frame_bytes is None:
            return
        with self._condition:
            self._latest_frame = frame_bytes
            self._frame_version += 1
            self._state = state
            self._last_error = error
            if state == "connected":
                self._last_frame_timestamp = time.time()
            self._condition.notify_all()

    def _publish_unavailable(self, message):
        self._publish(
            self._placeholder("RTSP stream unavailable"),
            state="reconnecting",
            error=message,
        )

    def _has_subscribers(self):
        with self._condition:
            return self._subscribers > 0

    def _create_capture(self):
        camera = self.capture_factory()
        try:
            camera.set(cv2.CAP_PROP_OPEN_TIMEOUT_MSEC, self.open_timeout_ms)
            camera.set(cv2.CAP_PROP_READ_TIMEOUT_MSEC, self.read_timeout_ms)
        except (AttributeError, cv2.error):
            pass
        opened = camera.open(self.url)
        return camera, bool(opened and camera.isOpened())

    def _run(self):
        reconnect_delay = self.reconnect_initial
        try:
            while self._has_subscribers():
                self._set_state("connecting")
                camera = None
                try:
                    camera, opened = self._create_capture()
                    if not opened:
                        self._publish_unavailable("无法打开 RTSP 地址")
                    else:
                        reconnect_delay = self.reconnect_initial
                        minimum_interval = 1.0 / self.frame_rate
                        last_publish = 0.0

                        while self._has_subscribers() and not self._stop_event.is_set():
                            success, frame = camera.read()
                            if not success:
                                self._publish_unavailable("RTSP 读取中断")
                                break

                            now = time.monotonic()
                            remaining = minimum_interval - (now - last_publish)
                            if remaining > 0 and self._stop_event.wait(remaining):
                                break

                            encoded, buffer = cv2.imencode(
                                ".jpg",
                                frame,
                                [cv2.IMWRITE_JPEG_QUALITY, self.jpeg_quality],
                            )
                            if encoded:
                                self._publish(buffer.tobytes())
                                last_publish = time.monotonic()
                except Exception as exc:
                    self._publish_unavailable(f"RTSP 线程异常：{type(exc).__name__}")
                finally:
                    if camera is not None:
                        camera.release()

                if self._has_subscribers():
                    if self._stop_event.wait(reconnect_delay):
                        break
                    reconnect_delay = min(reconnect_delay * 2, self.reconnect_max)
        finally:
            with self._condition:
                self._thread = None
                if self._subscribers > 0:
                    self._stop_event.clear()
                    self._thread = threading.Thread(
                        target=self._run,
                        name="helmet-rtsp-reader",
                        daemon=True,
                    )
                    self._thread.start()
                else:
                    self._state = "idle"
                self._condition.notify_all()

    def _subscribe(self):
        with self._condition:
            self._subscribers += 1
            self._stop_event.clear()
            if self._thread is None:
                self._thread = threading.Thread(
                    target=self._run,
                    name="helmet-rtsp-reader",
                    daemon=True,
                )
                self._thread.start()

    def _unsubscribe(self):
        with self._condition:
            self._subscribers = max(0, self._subscribers - 1)
            if self._subscribers == 0:
                self._stop_event.set()
                self._condition.notify_all()

    def generate(self):
        self._subscribe()
        last_version = -1
        try:
            while True:
                with self._condition:
                    self._condition.wait_for(
                        lambda: self._frame_version != last_version,
                        timeout=5,
                    )
                    frame = self._latest_frame
                    last_version = self._frame_version
                if frame is None:
                    continue
                yield (
                    b"--frame\r\n"
                    b"Content-Type: image/jpeg\r\n\r\n"
                    + frame
                    + b"\r\n"
                )
        finally:
            self._unsubscribe()

    def status(self):
        with self._condition:
            last_frame_at = None
            if self._last_frame_timestamp is not None:
                last_frame_at = datetime.fromtimestamp(
                    self._last_frame_timestamp,
                    tz=timezone.utc,
                ).isoformat()
            return {
                "state": self._state,
                "subscribers": self._subscribers,
                "last_frame_at": last_frame_at,
                "last_error": self._last_error,
            }
