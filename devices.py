"""Instrument classes used in the signal_lab demo project.

The goal of these classes is to provide a simple yet realistic API for
communicating with laboratory instruments.  Each instrument implements
`__enter__` and `__exit__` so they can be used as context managers, ensuring
that connections are properly opened and closed even when exceptions are
raised.  They also use properties to expose settings in a Pythonic way.
"""

from __future__ import annotations

import random
from typing import Optional

from exceptions import InstrumentError, ConnectionError, RangeError


class SignalGenerator:
    """A simple signal generator abstraction.

    Parameters
    ----------
    resource : str
        A resource identifier for the instrument (e.g., an IP address or GPIB
        string).  In this demo it is not used for real communications but
        illustrates where such information would belong.
    min_freq : float, optional
        Minimum allowed output frequency in hertz.  Defaults to 1e3 (1 kHz).
    max_freq : float, optional
        Maximum allowed output frequency in hertz.  Defaults to 1e9 (1 GHz).
    """

    def __init__(self, resource: str = "GPIB0::10", *, min_freq: float = 1e3, max_freq: float = 1e9) -> None:
        self.resource = resource
        self.min_freq = min_freq
        self.max_freq = max_freq
        self._frequency: Optional[float] = None
        self._connected: bool = False

    # Context manager methods ensure resources are always released
    def __enter__(self) -> "SignalGenerator":
        # In a real implementation, open the hardware connection here
        self._connected = True
        print(f"[SignalGenerator] Connected to {self.resource}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        # In a real implementation, close the hardware connection here
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
        """Set the output frequency of the signal generator.

        Raises
        ------
        RangeError
            If the given frequency is outside the allowed range.
        """
        if not (self.min_freq <= value <= self.max_freq):
            raise RangeError(
                f"Frequency {value} Hz is out of range ({self.min_freq}–{self.max_freq} Hz)"
            )
        self._frequency = value
        # Simulate sending a command to the instrument
        if self._connected:
            print(f"[SignalGenerator] Frequency set to {value:.0f} Hz")

    def enable_output(self) -> None:
        """Enable RF output."""
        self.check_connected()
        print("[SignalGenerator] Output ON")

    def disable_output(self) -> None:
        """Disable RF output."""
        self.check_connected()
        print("[SignalGenerator] Output OFF")


class SpectrumAnalyzer:


    """A simple spectrum analyzer abstraction.

    The spectrum analyzer can measure the frequency of a signal source.  It
    simulates measurement noise by adding a small random offset to the true
    frequency.
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

        Parameters
        ----------
        source : SignalGenerator
            The signal generator whose frequency is being measured.  The
            generator must be connected and have a frequency set.

        Returns
        -------
        float
            The measured frequency in hertz, including simulated noise.

        Raises
        ------
        InstrumentError
            If the analyzer or generator are not properly configured.
        """
        self.check_connected()
        source.check_connected()
        freq = source.frequency
        if freq is None:
            raise InstrumentError("Signal generator frequency is not set")
        # Simulate measurement noise within ±accuracy_hz
        offset = random.uniform(-self.accuracy_hz, self.accuracy_hz)
        measured = freq + offset
        print(f"[SpectrumAnalyzer] Measured frequency {measured:.2f} Hz (offset {offset:.2f} Hz)")
        return measured
    
class Oven:
    """A simple oven abstraction for temperature control.

    This class simulates an oven that can be set to a specific temperature.
    It uses context management to ensure proper resource handling.
    """

    
    def  __init__(self, resource:str, minTemp: float, maxTemp: float, connection: bool ):
        self._temp = None
        self.resource = resource
        self.minTemp = minTemp
        self.maxTemp = maxTemp

        # i think connection logic should be here after getting the connections details
        #  and protocol, should be used with DP for create an instance for communication protocol

        if not connection:
            return "unable to connect"

        self.connection = connection

    @property
    def temp(self) -> Optional[float]:
        return self._temp

    @temp.setter
    def temp(self, value:float, *args, **kwargs):
        if value < self.minTemp or value > self.maxTemp:
            raise RangeError(f"value: {value} is not in range, range is: [{self.minTemp}, {self.maxTemp}]")

        self._temp = value # send a SCPI command

    def __enter__(self) -> Oven:
        self.connect = True
        print(f"should create instance for connection")
        return self
    
    def __exit__(self):
        """If connection lost will close comm"""
        print(f"should close connection")
        return self

