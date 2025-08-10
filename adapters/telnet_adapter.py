from __future__ import annotations
import telnetlib
from typing import Optional
from devices.base import AdapterProtocol


class TelnetAdapter(AdapterProtocol):
    def __init__(self, host: str, port: int = 23, timeout: float = 5.0, encoding: str = "ascii") -> None:
        self.host = host
        self.port = port
        self.timeout = timeout
        self.encoding = encoding
        self._tn: Optional[telnetlib.Telnet] = None

    def connect(self) -> None:
        if self._tn is not None:
            return
        self._tn = telnetlib.Telnet(self.host, self.port, timeout=self.timeout)

    def disconnect(self) -> None:
        if self._tn is None:
            return
        try:
            self._tn.close()
        finally:
            self._tn = None

    def is_connected(self) -> bool:
        return self._tn is not None
