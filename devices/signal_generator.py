"""Signal generator device.

Override notes:
- Subclassing is uncommon; prefer composition. If subclassing, override context
  management carefully and call super().__enter__/__exit__.
"""

from __future__ import annotations

from typing import Optional

from core.exceptions import ConnectionError, RangeError


class SignalGenerator:
    """A simple signal generator abstraction.

    Parameters
    ----------
    resource : str
        Resource identifier for the instrument.
    min_freq : float
        Minimum frequency in Hz.
    max_freq : float
        Maximum frequency in Hz.
    """

    def __init__(self, resource: str = "GPIB0::10", *, min_freq: float = 1e3, max_freq: float = 1e9) -> None:
        self.resource = resource
        self.min_freq = min_freq
        self.max_freq = max_freq
        self._frequency: Optional[float] = None
        self._connected: bool = False

    def __enter__(self) -> "SignalGenerator":
        self._connected = True
        print(f"[SignalGenerator] Connected to {self.resource}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if self._connected:
            print(f"[SignalGenerator] Disconnected from {self.resource}")
            self._connected = False

    def check_connected(self) -> None:
        if not self._connected:
            raise ConnectionError("Signal generator is not connected")

    @property
    def frequency(self) -> Optional[float]:
        """Current output frequency in hertz, or None if not set."""
        return self._frequency

    @frequency.setter
    def frequency(self, value: float) -> None:
        if not (self.min_freq <= value <= self.max_freq):
            raise RangeError(
                f"Frequency {value} Hz is out of range ({self.min_freq}–{self.max_freq} Hz)"
            )
        self._frequency = value
        if self._connected:
            print(f"[SignalGenerator] Frequency set to {value:.0f} Hz")

    def enable_output(self) -> None:
        self.check_connected()
        print("[SignalGenerator] Output ON")

    def disable_output(self) -> None:
        self.check_connected()
        print("[SignalGenerator] Output OFF")
