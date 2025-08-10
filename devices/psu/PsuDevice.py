from typing import Dict, Optional, Union
from ..base import BaseDevice, AdapterProtocol, ConfigLoaderProtocol
from .strategy import (
    PsuStrategy,
    PSUContext,
    VirtualPsuStrategy,
)


class PSU(BaseDevice):
    def __init__(self, model: str, adapter: AdapterProtocol, config_loader: ConfigLoaderProtocol, *, strategy: Optional[PsuStrategy] = None) -> None:
        self._listActions = ["voltage", "current", "temp", "output"]

        if adapter is None:
            raise ValueError("adapter is required")
        if not model:
            raise ValueError("model is required")
        if config_loader is None:
            raise ValueError("config loader is required")

        super().__init__(model, adapter, config_loader)
        self.device_type = "psu"

        self._capabilities = self.config_loader.load_capabilities(self.model)
        self._ranges = self.config_loader.load_ranges(self.model)

        # Strategy selection: default to Virtual if not provided
        self._strategy = strategy or VirtualPsuStrategy()
        self._strategy.attach(PSUContext(capabilities=self._capabilities, ranges=self._ranges))

    def connect(self) -> None:
        super().connect()
        # Initialize underlying strategy after transport connect
        self._strategy.initialize()

    def disconnect(self) -> None:
        super().disconnect()

    def get_state(self) -> str:
        return self.state.name.lower()

    def get_capabilities(self) -> Dict[str, bool]:
        return self._capabilities

    def read(self, key: str) -> Union[float, bool]:
        self.require_connected()
        if key not in self._listActions:
            raise KeyError(f"unable to read {key}; allowed: {self._listActions}")
        return self._strategy.read(key)

    def set(self, key: str, value: object) -> None:
        self.require_connected()
        # capability gates
        def _cap(name: str) -> bool:
            return bool(self._capabilities.get(name, False))

        if key == "voltage":
            if not _cap("set_voltage"):
                raise PermissionError("set_voltage not supported by this model")
            self._strategy.set_voltage(float(value))
            return None
        if key == "current_limit":
            if not _cap("set_current_limit"):
                raise PermissionError("set_current_limit not supported by this model")
            self._strategy.set_current_limit(float(value))
            return None
        if key == "output":
            if not _cap("toggle_output"):
                raise PermissionError("toggle_output not supported by this model")
            self._strategy.toggle_output(bool(value))
            return None
        if key == "power_cycle":
            if not _cap("power_cycle"):
                raise PermissionError("power_cycle not supported by this model")
            self._strategy.power_cycle()
            return None
        raise KeyError(f"unknown set key: {key}")