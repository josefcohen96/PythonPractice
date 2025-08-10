from __future__ import annotations
from typing import Optional
from devices.base import AdapterProtocol

try:
    import paramiko
except Exception:  # pragma: no cover - optional dependency
    paramiko = None  # type: ignore


class SSHAdapter(AdapterProtocol):
    def __init__(self, host: str, username: str, password: str, port: int = 22, timeout: float = 5.0) -> None:
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.timeout = timeout
        self._client = None  # client will be a paramiko.SSHClient when connected

    def connect(self) -> None:
        if self._client is not None:
            return
        if paramiko is None:
            raise RuntimeError("paramiko is required for SSHAdapter")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(self.host, port=self.port, username=self.username, password=self.password, timeout=self.timeout)
        self._client = client

    def disconnect(self) -> None:
        if self._client is None:
            return
        try:
            self._client.close()
        finally:
            self._client = None

    def is_connected(self) -> bool:
        return self._client is not None
