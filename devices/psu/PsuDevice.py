from typing import Dict, Optional, Union
from devices.base import BaseDevice, AdapterProtocol, ConfigLoaderProtocol
from .strategy import (
    PsuStrategy,
    PSUContext,
    VirtualPsuStrategy,
)
from devices.base.BaseDevice import DeviceBehavior, DeviceContext


class PsuDeviceBehavior(DeviceBehavior):
    def __init__(self, strategy: Optional[PsuStrategy] = None) -> None:
        self._strategy: PsuStrategy = strategy or VirtualPsuStrategy()
        self._capabilities: Dict[str, bool] = {}
        self._ranges: Dict[str, Dict[str, Union[float, str]]] = {}
        self._listActions = ["voltage", "current", "temp", "output"]

    def attach(self, ctx: DeviceContext) -> None:
        self._capabilities = dict(ctx.capabilities)
        self._ranges = dict(ctx.ranges)
        self._strategy.attach(PSUContext(capabilities=self._capabilities, ranges=self._ranges))

    def initialize(self) -> None:
        self._strategy.initialize()

    def get_capabilities(self) -> Dict[str, bool]:
        return self._capabilities

    def read(self, key: str) -> Union[float, bool]:
        if key not in self._listActions:
            raise KeyError(f"unable to read {key}; allowed: {self._listActions}")
        return self._strategy.read(key)

    def set(self, key: str, value: object) -> None:
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


class PSU:
    def __init__(self, model: str, adapter: AdapterProtocol, config_loader: ConfigLoaderProtocol, *, strategy: Optional[PsuStrategy] = None) -> None:
        if adapter is None:
            raise ValueError("adapter is required")
        if not model:
            raise ValueError("model is required")
        if config_loader is None:
            raise ValueError("config loader is required")

        behavior = PsuDeviceBehavior(strategy=strategy or VirtualPsuStrategy())
        self._device = BaseDevice(model, adapter, config_loader, behavior)
        self.device_type = "psu"

    # Proxy API to underlying BaseDevice
    @property
    def state(self) -> str:
        return self._device.state

    @property
    def is_connected(self) -> bool:
        return self._device.is_connected

    def connect(self) -> None:
        self._device.connect()

    def disconnect(self) -> None:
        self._device.disconnect()

    def get_state(self) -> str:
        return self._device.get_state()

    def get_capabilities(self) -> Dict[str, bool]:
        return self._device.get_capabilities()

    def read(self, key: str) -> Union[float, bool]:
        return self._device.read(key)

    def set(self, key: str, value: object) -> None:
        self._device.set(key, value)