from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass(frozen=True)
class Credentials:
    username: str
    salt: str
    password_hash: str


class CredentialsStore:
    def __init__(self, file_path: Path) -> None:
        self._file_path = file_path

    def load(self) -> Optional[Credentials]:
        if not self._file_path.exists():
            return None
        payload = json.loads(self._file_path.read_text(encoding="utf-8"))
        return Credentials(
            username=payload["username"],
            salt=payload["salt"],
            password_hash=payload["password_hash"],
        )

    def save(self, username: str, password: str) -> None:
        salt = os.urandom(16).hex()
        password_hash = self._hash_password(password, salt)
        payload = {"username": username, "salt": salt, "password_hash": password_hash}
        self._file_path.parent.mkdir(parents=True, exist_ok=True)
        self._file_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    def verify(self, username: str, password: str) -> bool:
        credentials = self.load()
        if credentials is None:
            return False
        if credentials.username != username:
            return False
        return credentials.password_hash == self._hash_password(password, credentials.salt)

    @staticmethod
    def _hash_password(password: str, salt: str) -> str:
        return hashlib.sha256(f"{salt}:{password}".encode("utf-8")).hexdigest()
