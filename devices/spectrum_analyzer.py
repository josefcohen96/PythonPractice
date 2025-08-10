"""Spectrum analyzer device.

Override notes:
- If subclassing to add real IO, override measure_frequency() and use
  check_connected() before IO. Keep accuracy_hz semantics.
"""

from __future__ import annotations

import random

from core.exceptions import InstrumentError, ConnectionError
from .signal_generator import SignalGenerator


class SpectrumAnalyzer:
    """A simple spectrum analyzer abstraction.

    Measures frequency of a signal source with simulated noise.
    """

    def __init__(self, resource: str = "GPIB0::20", *, accuracy_hz: float = 1.0) -> None:
        self.resource = resource
        self.accuracy_hz = accuracy_hz
        self._connected: bool = False

    def __enter__(self) -> "SpectrumAnalyzer":
        self._connected = True
        print(f"[SpectrumAnalyzer] Connected to {self.resource}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if self._connected:
            print(f"[SpectrumAnalyzer] Disconnected from {self.resource}")
            self._connected = False

    def check_connected(self) -> None:
        if not self._connected:
            raise ConnectionError("Spectrum analyzer is not connected")

    def measure_frequency(self, source: SignalGenerator) -> float:
        """Measure the output frequency of a signal generator.

        Raises InstrumentError if preconditions are not met.
        """
        self.check_connected()
        source.check_connected()
        freq = source.frequency
        if freq is None:
            raise InstrumentError("Signal generator frequency is not set")
        offset = random.uniform(-self.accuracy_hz, self.accuracy_hz)
        measured = freq + offset
        print(f"[SpectrumAnalyzer] Measured frequency {measured:.2f} Hz (offset {offset:.2f} Hz)")
        return measured
