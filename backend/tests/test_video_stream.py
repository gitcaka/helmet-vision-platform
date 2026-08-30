import time
import unittest

import numpy as np

from video_stream import SharedVideoStream


class FakeCapture:
    def __init__(self):
        self.opened = False
        self.released = False

    def set(self, _property, _value):
        return True

    def open(self, _url):
        self.opened = True
        return True

    def isOpened(self):
        return self.opened and not self.released

    def read(self):
        return True, np.full((32, 48, 3), 120, dtype=np.uint8)

    def release(self):
        self.released = True


class SharedVideoStreamTestCase(unittest.TestCase):
    def test_two_clients_share_one_capture(self):
        captures = []

        def capture_factory():
            capture = FakeCapture()
            captures.append(capture)
            return capture

        stream = SharedVideoStream(
            "rtsp://example.test/output",
            frame_rate=30,
            reconnect_initial=0.01,
            reconnect_max=0.02,
            capture_factory=capture_factory,
        )
        first = stream.generate()
        second = stream.generate()
        self.assertIn(b"Content-Type: image/jpeg", next(first))
        self.assertIn(b"Content-Type: image/jpeg", next(second))

        deadline = time.monotonic() + 1
        while stream.status()["state"] != "connected" and time.monotonic() < deadline:
            time.sleep(0.01)

        self.assertEqual(stream.status()["subscribers"], 2)
        self.assertEqual(stream.status()["state"], "connected")
        self.assertEqual(len(captures), 1)

        first.close()
        second.close()
        deadline = time.monotonic() + 1
        while stream.status()["state"] != "idle" and time.monotonic() < deadline:
            time.sleep(0.01)
        self.assertEqual(stream.status()["subscribers"], 0)
        self.assertEqual(stream.status()["state"], "idle")
        self.assertTrue(captures[0].released)


if __name__ == "__main__":
    unittest.main()
