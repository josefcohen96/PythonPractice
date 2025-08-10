from __future__ import annotations

import random
import time
from abc import ABC, abstractmethod
from typing import Dict, Optional, Callable

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

    # Context is a lightweight view the strategy needs: capabilities, ranges, etc.
    def attach(self, ctx: "PSUContext") -> None:
        self._ctx = ctx

    @abstractmethod
    def initialize(self) -> None:
        ...

    @abstractmethod
    def read(self, key: str) -> float | bool:
        ...

    @abstractmethod
    def set_voltage(self, volts: float) -> None:
        ...

    @abstractmethod
    def set_current_limit(self, amps: float) -> None:
        ...

    @abstractmethod
    def toggle_output(self, on: bool) -> None:
        ...

    @abstractmethod
    def power_cycle(self) -> None:
        ...


class PSUContext:
    """Context shared with strategies (no strong coupling to BaseDevice)."""

    def __init__(self, *, capabilities: Dict[str, bool], ranges: Dict[str, Dict[str, float | str]]) -> None:
        self.capabilities = capabilities
        self.ranges = ranges


class VirtualPsuStrategy(PsuStrategy):
    """Purely simulated PSU behavior with simple physics and delays."""

    def __init__(self) -> None:
        super().__init__()
        self._voltage_sp: float = 0.0
        self._current_limit: float = 0.0
        self._output_on: bool = False
        self._temp_c: float = 25.0

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

    def read(self, key: str) -> float | bool:
        if key == "voltage":
            # If output on, assume measured voltage approaches setpoint
            noise = random.uniform(-0.01, 0.01)
            return max(0.0, self._voltage_sp + noise) if self._output_on else 0.0
        if key == "current":
            # Simple model: small current draw proportional to voltage
            return self._current_limit if self._output_on and self._current_limit < 0.1 else (
                0.05 if self._output_on and self._voltage_sp > 0 else 0.0
            )
        if key == "temp":
            # Drift temperature slightly when on
            self._temp_c += 0.01 if self._output_on else -0.005
            return max(20.0, min(60.0, self._temp_c))
        if key == "output":
            return self._output_on
        raise KeyError(f"Unknown read key: {key}")

    def set_voltage(self, volts: float) -> None:
        if not self._in_range("voltage", volts):
            raise ValueError(f"voltage out of range: {volts}")
        # Busy for ~100ms per spec
        time.sleep(SET_VOLTAGE_DELAY_S)
        self._voltage_sp = volts

    def set_current_limit(self, amps: float) -> None:
        if not self._in_range("current", amps):
            raise ValueError(f"current limit out of range: {amps}")
        self._current_limit = amps

    def toggle_output(self, on: bool) -> None:
        # Delay 500ms when turning ON to simulate stabilization
        if on and not self._output_on:
            time.sleep(OUTPUT_ON_DELAY_S)
        self._output_on = on

    def power_cycle(self) -> None:
        # 5 seconds busy cycle
        if self._output_on:
            self._output_on = False
        time.sleep(POWER_CYCLE_DELAY_S)
        self._output_on = True


class RealPsuStrategy(PsuStrategy):
    """Represents a real PSU. If no transport IO is provided, falls back to simple stateful behavior.

    This keeps the API stable while allowing real IO integration later.
    """

    def __init__(self, *, write: Callable[[str], None] | None = None, read: Callable[[str], str] | None = None) -> None:
        super().__init__()
        self._write = write  # optional callables for instrument IO
        self._read = read
        self._mirror = VirtualPsuStrategy()  # fallback behavior

    def attach(self, ctx: PSUContext) -> None:
        super().attach(ctx)
        self._mirror.attach(ctx)

    def initialize(self) -> None:
        # If we had IO, we could query IDN?, reset, etc.
        self._mirror.initialize()

    def read(self, key: str) -> float | bool:
        # If real IO available, map reads to SCPI (e.g., MEAS:VOLT?)
        # For now, fallback to mirror
        return self._mirror.read(key)

    def set_voltage(self, volts: float) -> None:
        # If real IO available: self._write(f"VOLT {volts}")
        self._mirror.set_voltage(volts)

    def set_current_limit(self, amps: float) -> None:
        # If real IO available: self._write(f"CURR {amps}")
        self._mirror.set_current_limit(amps)

    def toggle_output(self, on: bool) -> None:
        # If real IO available: self._write(f"OUTP {'ON' if on else 'OFF'}")
        self._mirror.toggle_output(on)

    def power_cycle(self) -> None:
        # If real IO available: sequence relays; here we simulate
        self._mirror.power_cycle()
