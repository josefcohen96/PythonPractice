from __future__ import annotations
from typing import Optional
from devices.base import AdapterProtocol

try:  # Python 3.13 may not include telnetlib (PEP 594)
    import telnetlib  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    telnetlib = None  # type: ignore


class TelnetAdapter(AdapterProtocol):
    def __init__(self, host: str, port: int = 23, timeout: float = 5.0, encoding: str = "ascii") -> None:
        self.host = host
        self.port = port
        self.timeout = timeout
        self.encoding = encoding
        self._tn: Optional[object] = None

    def connect(self) -> None:
        if self._tn is not None:
            return
        if telnetlib is None:
            raise RuntimeError("telnetlib is required for TelnetAdapter")
        self._tn = telnetlib.Telnet(self.host, self.port, timeout=self.timeout)

    def disconnect(self) -> None:
        if self._tn is None:
            return
        try:
            # Defer attribute access until runtime to avoid hard dependency
            close = getattr(self._tn, "close", None)
            if callable(close):
                close()
        finally:
            self._tn = None

    def is_connected(self) -> bool:
        return self._tn is not None
