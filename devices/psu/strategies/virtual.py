from __future__ import annotations

import random
import time
from typing import Union

from .base import PsuStrategy, PSUContext, SET_VOLTAGE_DELAY_S, OUTPUT_ON_DELAY_S, POWER_CYCLE_DELAY_S


class VirtualPsuStrategy(PsuStrategy):
    """Purely simulated PSU behavior with simple physics and delays."""

    def __init__(self) -> None:
        super().__init__()
        self._voltage_sp: float = 0.0
        self._current_limit: float = 0.0
        self._output_on: bool = False
        self._temp_c: float = 25.0
        self._rng = random.Random()  # For noise simulation

    def initialize(self) -> None:
        # Nothing special to do for a virtual PSU
        pass

    # Helpers
    def _in_range(self, key: str, value: float) -> bool:
        rng = self._ctx.ranges.get(key, {}) if self._ctx else {}
        try:
            return float(rng.get("min", float("-inf"))) <= value <= float(rng.get("max", float("inf")))
        except Exception:
            return True

    def read(self, key: str) -> Union[float, bool]:
        if key == "voltage":
            if not self._output_on:
                return 0.0
            noisy = self._voltage_sp + self._rng.uniform(-0.1, 0.1)
            return max(noisy, 0.0)
        if key == "current":
            if not self._output_on:
                return 0.0
            noisy = self._current_limit + self._rng.uniform(-0.01, 0.01)
            return max(noisy, 0.0)
        if key == "temp":
            if not self._output_on:
                return 0.0
            noisy = self._temp_c + self._rng.uniform(-1.0, 1.0)
            return max(noisy, 0.0)
        if key == "output":
            return self._output_on

    def set_voltage(self, volts: float) -> None:
        if not self._in_range("voltage", volts):
            raise ValueError(f"voltage out of range: {volts}")
        time.sleep(SET_VOLTAGE_DELAY_S)
        self._voltage_sp = volts

    def set_current_limit(self, amps: float) -> None:
        if not self._in_range("current", amps):
            raise ValueError(f"current limit out of range: {amps}")
        self._current_limit = amps

    def toggle_output(self, on: bool) -> None:
        if on and not self._output_on:
            time.sleep(OUTPUT_ON_DELAY_S)
        self._output_on = on

    def power_cycle(self) -> None:
        if self._output_on:
            self._output_on = False
        time.sleep(POWER_CYCLE_DELAY_S)
        self._output_on = True