from __future__ import annotations
from typing import Mapping, Optional, Union, Tuple

from ..base import BaseDevice, AdapterProtocol, ConfigLoaderProtocol
from .strategies import (
    PsuStrategy,
    PSUContext,
    VirtualPsuStrategy,
)


class PSU(BaseDevice):
    """
    PSU device with a property-based API (voltage/current_limit/output).
    Keeps a backwards-compatible .set(key, value) method that dispatches to
    the typed properties. All setters gate by capabilities and ranges and
    delegate to the selected strategy.
    """

    _ALLOWED_READS: Tuple[str, ...] = ("voltage", "current", "temp", "output")

    def __init__(
        self,
        model: str,
        adapter: AdapterProtocol,
        config_loader: ConfigLoaderProtocol,
        strategy: Optional[PsuStrategy] = None,
    ) -> None:
        if adapter is None:
            raise ValueError("adapter is required")
        if not model:
            raise ValueError("model is required")
        if config_loader is None:
            raise ValueError("config loader is required")

        super().__init__(model, adapter, config_loader)
        self.device_type = "psu"

        self._capabilities: Mapping[str, bool] = self.config_loader.load_capabilities(self.model)
        self._ranges: Mapping[str, Mapping[str, float]] = self.config_loader.load_ranges(self.model)

        self._strategy: PsuStrategy = strategy or VirtualPsuStrategy()
        self._strategy.attach(PSUContext(capabilities=self._capabilities, ranges=self._ranges))

        self._voltage_set: float = 0.0
        self._current_limit_set: float = 0.0
        self._output_set: bool = False

    def _on_connect(self) -> None:
        self._strategy.initialize()

    def get_state(self) -> str:
        return self.state.name.lower()

    def get_capabilities(self) -> Mapping[str, bool]:
        return self._capabilities

    @property
    def voltage(self) -> float:
        return self._voltage_set

    @voltage.setter
    def voltage(self, v: float) -> None:
        self.require_connected()
        if not self._capabilities.get("set_voltage", False):
            raise PermissionError("set_voltage not supported by this model")
        v = float(v)
        lo, hi = self._ranges["voltage"]["min"], self._ranges["voltage"]["max"]
        if not (lo <= v <= hi):
            raise ValueError(f"voltage out of range {lo}..{hi}")
        self._strategy.set_voltage(v)
        self._voltage_set = v

    @property
    def current_limit(self) -> float:
        return self._current_limit_set

    @current_limit.setter
    def current_limit(self, a: float) -> None:
        self.require_connected()
        if not self._capabilities.get("set_current_limit", False):
            raise PermissionError("set_current_limit not supported by this model")
        a = float(a)
        self._strategy.set_current_limit(a)
        self._current_limit_set = a

    @property
    def output(self) -> bool:
        return self._output_set

    @output.setter
    def output(self, on: bool) -> None:
        self.require_connected()
        if not self._capabilities.get("toggle_output", False):
            raise PermissionError("toggle_output not supported by this model")
        on = bool(on)
        self._strategy.toggle_output(on)
        self._output_set = on

    def read_voltage(self) -> float:
        self.require_connected()
        return float(self._strategy.read("voltage"))

    def read_current(self) -> float:
        self.require_connected()
        return float(self._strategy.read("current"))

    def read_temp(self) -> float | None:
        self.require_connected()
        val = self._strategy.read("temp")
        return None if val is None else float(val)

    def read(self, key: str) -> Union[float, bool, None]:
        self.require_connected()
        if key not in self._ALLOWED_READS:
            raise KeyError(f"unable to read {key}; allowed: {self._ALLOWED_READS}")
        if key == "voltage":
            return self.read_voltage()
        if key == "current":
            return self.read_current()
        if key == "temp":
            return self.read_temp()
        if key == "output":
            return bool(self._strategy.read("output"))
        raise KeyError(f"unknown read key: {key}")

    def set(self, key: str, value: object) -> None:
        self.require_connected()
        if key == "voltage":
            self.voltage = float(value)
            return
        if key == "current_limit":
            self.current_limit = float(value)
            return
        if key == "output":
            self.output = bool(value)
            return
        if key == "power_cycle":
            if not self._capabilities.get("power_cycle", False):
                raise PermissionError("power_cycle not supported by this model")
            self._strategy.power_cycle()
            return
        raise KeyError(f"unknown set key: {key}")