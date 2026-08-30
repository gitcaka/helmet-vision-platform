import os
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch


_temporary_directory = tempfile.TemporaryDirectory(prefix="helmet-flask-test-")
os.environ["HELMET_DATABASE_PATH"] = str(
    Path(_temporary_directory.name) / "helmet-test.db"
)
os.environ["HELMET_INGEST_API_TOKEN"] = "verification-token"
os.environ["HELMET_DATA_RECONCILE_INTERVAL"] = "0.05"

from app import app, socketio  # noqa: E402
from models import Log, Traffic, User, db  # noqa: E402


class HelmetAppTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config.update(TESTING=True)

    @classmethod
    def tearDownClass(cls):
        with app.app_context():
            db.session.remove()
            db.engine.dispose()
        _temporary_directory.cleanup()

    def setUp(self):
        with app.app_context():
            db.drop_all()
            db.create_all()
            user = User(username="admin")
            user.set_password("StrongPass123!")
            db.session.add(user)
            db.session.commit()
        self.client = app.test_client()
        self.headers = {"X-API-Token": "verification-token"}

    def login(self):
        return self.client.post(
            "/login",
            json={"username": "admin", "password": "StrongPass123!"},
        )

    def test_login_session_protects_data_video_and_socketio(self):
        self.assertEqual(self.client.get("/api/data").status_code, 401)
        self.assertEqual(self.client.get("/video_feed").status_code, 401)

        anonymous_socket = socketio.test_client(app)
        self.assertFalse(anonymous_socket.is_connected())

        login = self.login()
        self.assertEqual(login.status_code, 200)
        user = login.get_json()["text"]
        self.assertEqual(user["username"], "admin")
        self.assertNotIn("password", user)
        self.assertNotIn("password_hash", user)
        self.assertEqual(self.client.get("/api/me").status_code, 200)
        self.assertEqual(self.client.get("/api/data").status_code, 200)

        socket_client = socketio.test_client(app, flask_test_client=self.client)
        self.assertTrue(socket_client.is_connected())
        received = socket_client.get_received()
        self.assertTrue(any(item["name"] == "data_update" for item in received))
        socket_client.disconnect()
        time.sleep(0.1)

        self.assertEqual(self.client.post("/logout").status_code, 200)
        self.assertEqual(self.client.get("/api/me").status_code, 401)

    def test_wrong_password_is_rejected(self):
        rejected = self.client.post(
            "/login",
            json={"username": "admin", "password": "wrong-password"},
        )
        self.assertEqual(rejected.status_code, 401)

    def test_repeated_login_failures_are_rate_limited(self):
        for _ in range(app.config["LOGIN_MAX_ATTEMPTS"]):
            response = self.client.post(
                "/login",
                json={"username": "rate-limit-user", "password": "wrong-password"},
            )
            self.assertEqual(response.status_code, 401)

        limited = self.client.post(
            "/login",
            json={"username": "rate-limit-user", "password": "wrong-password"},
        )
        self.assertEqual(limited.status_code, 429)
        self.assertGreater(limited.get_json()["retry_after"], 0)

    def test_ingest_api_is_disabled_without_server_token(self):
        with patch.dict(app.config, {"INGEST_API_TOKEN": ""}):
            response = self.client.post(
                "/api/logs",
                json={"event_id": "disabled-token-event", "type": "helmet"},
            )
        self.assertEqual(response.status_code, 503)

    def test_log_write_is_idempotent(self):
        body = {
            "event_id": "camera-01-20260830-0001",
            "type": "noHelmet",
            "camera": "camera-01",
            "score": 0.97,
            "location": "north-gate",
        }
        created = self.client.post("/api/logs", headers=self.headers, json=body)
        duplicate = self.client.post("/api/logs", headers=self.headers, json=body)

        self.assertEqual(created.status_code, 201)
        self.assertFalse(created.get_json()["duplicate"])
        self.assertEqual(duplicate.status_code, 200)
        self.assertTrue(duplicate.get_json()["duplicate"])
        with app.app_context():
            self.assertEqual(Log.query.count(), 1)

    def test_committed_write_survives_socket_failure(self):
        body = {
            "event_id": "camera-01-20260830-emit-failure",
            "type": "helmet",
        }
        with patch.object(socketio, "emit", side_effect=RuntimeError("offline")):
            with patch.object(app.logger, "exception"):
                response = self.client.post(
                    "/api/logs",
                    headers=self.headers,
                    json=body,
                )

        self.assertEqual(response.status_code, 201)
        with app.app_context():
            self.assertEqual(Log.query.count(), 1)

    def test_traffic_validation_and_upsert(self):
        invalid = self.client.post(
            "/api/traffic",
            headers=self.headers,
            json={
                "date": "2026-08-30",
                "total": 5,
                "ele": 6,
                "helmet": 4,
                "noHelmet": 2,
            },
        )
        self.assertEqual(invalid.status_code, 400)

        created = self.client.post(
            "/api/traffic",
            headers=self.headers,
            json={
                "date": "2026-08-30",
                "total": 10,
                "ele": 8,
                "helmet": 6,
                "noHelmet": 2,
            },
        )
        updated = self.client.post(
            "/api/traffic",
            headers=self.headers,
            json={
                "date": "2026-08-30",
                "total": 11,
                "ele": 9,
                "helmet": 7,
                "noHelmet": 2,
            },
        )
        self.assertEqual(created.status_code, 201)
        self.assertEqual(updated.status_code, 200)
        with app.app_context():
            self.assertEqual(Traffic.query.count(), 1)
            self.assertEqual(Traffic.query.first().total, 11)

    def test_health_reports_video_state(self):
        health = self.client.get("/health")
        self.assertEqual(health.status_code, 200)
        data = health.get_json()
        self.assertEqual(data["database"], "sqlite")
        self.assertIn("state", data["video"])


if __name__ == "__main__":
    unittest.main()
