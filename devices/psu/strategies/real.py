from __future__ import annotations

from typing import Callable, Optional, Union

from .base import PsuStrategy, PSUContext
from .virtual import VirtualPsuStrategy


class RealPsuStrategy(PsuStrategy):
    """Represents a real PSU. If no transport IO is provided, falls back to simple stateful behavior.

    This keeps the API stable while allowing real IO integration later.
    """

    def __init__(self, *, write: Optional[Callable[[str], None]] = None, read: Optional[Callable[[str], str]] = None) -> None:
        super().__init__()
        self._write = write
        self._read = read
        self._mirror = VirtualPsuStrategy()

    def attach(self, ctx: PSUContext) -> None:
        super().attach(ctx)
        self._mirror.attach(ctx)

    def initialize(self) -> None:
        self._mirror.initialize()

    def read(self, key: str) -> Union[float, bool]:
        return self._mirror.read(key)

    def set_voltage(self, volts: float) -> None:
        self._mirror.set_voltage(volts)

    def set_current_limit(self, amps: float) -> None:
        self._mirror.set_current_limit(amps)

    def toggle_output(self, on: bool) -> None:
        self._mirror.toggle_output(on)

    def power_cycle(self) -> None:
        self._mirror.power_cycle()