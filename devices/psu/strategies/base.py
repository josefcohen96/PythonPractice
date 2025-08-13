from __future__ import annotations

import time
from abc import ABC, abstractmethod
from typing import Dict, Optional, Union

# Operation delays (seconds)
SET_VOLTAGE_DELAY_S = 0.1
OUTPUT_ON_DELAY_S = 0.5
POWER_CYCLE_DELAY_S = 5.0


class PsuStrategy(ABC):
    """Strategy interface for PSU behaviors (real vs virtual).

    Override notes:
    - Implementations must enforce range/capability checks or expect caller to.
    - Keep methods fast; long operations should be documented.
    """

    def __init__(self) -> None:
        self._ctx: Optional["PSUContext"] = None

    def attach(self, ctx: "PSUContext") -> None:
        self._ctx = ctx

    @abstractmethod
    def initialize(self) -> None: ...

    @abstractmethod
    def read(self, key: str) -> Union[float, bool]: ...

    @abstractmethod
    def set_voltage(self, volts: float) -> None: ...

    @abstractmethod
    def set_current_limit(self, amps: float) -> None: ...

    @abstractmethod
    def toggle_output(self, on: bool) -> None: ...

    @abstractmethod
    def power_cycle(self) -> None: ...


class PSUContext:
    """Context shared with strategies (capabilities, ranges)."""

    def __init__(self, *, capabilities: Dict[str, bool], ranges: Dict[str, Dict[str, Union[float, str]]]) -> None:
        self.capabilities = capabilities
        self.ranges = ranges