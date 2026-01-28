import json
import tempfile
import unittest
from pathlib import Path

from app.infrastructure.credentials_store import CredentialsStore


class TestCredentialsStore(unittest.TestCase):
    def test_credentials_store_roundtrip(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "credentials.json"
            store = CredentialsStore(path)

            self.assertIsNone(store.load())

            store.save("user1", "secret")
            self.assertTrue(store.verify("user1", "secret"))
            self.assertFalse(store.verify("user1", "wrong"))
            self.assertFalse(store.verify("other", "secret"))

            payload = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(payload["username"], "user1")
            self.assertIn("password_hash", payload)


if __name__ == "__main__":
    unittest.main()
