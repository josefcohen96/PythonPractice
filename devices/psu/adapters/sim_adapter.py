from __future__ import annotations
import time
from devices.base import AdapterProtocol


class SimAdapter(AdapterProtocol):
    def __init__(self, connect_delay_s: float = 0.0, should_fail: bool = False) -> None:
        self._connected = False
        self.connect_delay_s = connect_delay_s
        self.should_fail = should_fail

    def connect(self) -> None:
        if self._connected:
            return
        if self.connect_delay_s:
            time.sleep(self.connect_delay_s)
        if self.should_fail:
            raise RuntimeError("simulated connect failure")
        self._connected = True

    def disconnect(self) -> None:
        if not self._connected:
            return
        self._connected = False

    def is_connected(self) -> bool:
        return self._connected

    # Convenience for tests that check driver.opened
    @property
    def opened(self) -> bool:
        return self._connected