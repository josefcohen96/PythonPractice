from __future__ import annotations
from abc import ABC
from enum import Enum, auto
from typing import Dict, Optional, Protocol

from core.exceptions import ConnectionError


class AdapterProtocol(Protocol):
    def connect(self) -> None: ...
    def disconnect(self) -> None: ...
    def is_connected(self) -> bool: ...


class ConfigLoaderProtocol(Protocol):
    def load_capabilities(self, model: str) -> Dict[str, bool]: ...
    def load_ranges(self, model: str) -> Dict[str, Dict[str, float | str]]: ...


class DeviceContext:
    def __init__(self, *, capabilities: Dict[str, bool], ranges: Dict[str, Dict[str, float | str]]) -> None:
        self.capabilities = capabilities
        self.ranges = ranges


class DeviceBehavior(Protocol):
    def attach(self, ctx: DeviceContext) -> None: ...
    def initialize(self) -> None: ...
    def get_capabilities(self) -> Dict[str, bool]: ...
    def read(self, key: str) -> object: ...
    def set(self, key: str, value: object) -> None: ...


class DeviceState(Enum):
    DISCONNECTED = auto()
    CONNECTING = auto()
    CONNECTED = auto()
    DISCONNECTING = auto()
    ERROR = auto()


class BaseDevice(ABC):
    """Device shell that manages connection lifecycle and delegates operations
    to a provided behavior strategy via composition.
    """

    def __init__(self, model: str, adapter: AdapterProtocol, config_loader: ConfigLoaderProtocol, behavior: DeviceBehavior) -> None:
        self.model = model
        self.adapter = adapter
        self.config_loader = config_loader
        self._state: DeviceState = DeviceState.DISCONNECTED

        # Load configuration and attach behavior
        capabilities = self.config_loader.load_capabilities(self.model)
        ranges = self.config_loader.load_ranges(self.model)
        self._behavior = behavior
        self._behavior.attach(DeviceContext(capabilities=capabilities, ranges=ranges))

    @property
    def state(self) -> DeviceState:
        return self._state

    @property
    def is_connected(self) -> bool:
        return self._state is DeviceState.CONNECTED

    def connect(self) -> None:
        if self.is_connected:
            return
        self._state = DeviceState.CONNECTING
        try:
            self.adapter.connect()
            self._behavior.initialize()
            self._state = DeviceState.CONNECTED
        except Exception as exc:
            self._state = DeviceState.ERROR
            raise ConnectionError(f"Connect error: {exc}") from exc

    def disconnect(self) -> None:
        if self._state is DeviceState.DISCONNECTED:
            return
        self._state = DeviceState.DISCONNECTING
        try:
            self.adapter.disconnect()
            self._state = DeviceState.DISCONNECTED
        except Exception as exc:
            self._state = DeviceState.ERROR
            raise ConnectionError(f"Disconnect error: {exc}") from exc

    def require_connected(self) -> None:
        if not self.is_connected:
            raise ConnectionError("Device is not connected")

    def get_state(self) -> str:
        return self.state.name.lower()

    def get_capabilities(self) -> Dict[str, bool]:
        return self._behavior.get_capabilities()

    def read(self, key: str) -> object:
        self.require_connected()
        return self._behavior.read(key)

    def set(self, key: str, value: object) -> None:
        self.require_connected()
        self._behavior.set(key, value)
