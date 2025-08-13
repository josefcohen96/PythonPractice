from __future__ import annotations
from abc import ABC, abstractmethod
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


class DeviceState(Enum):
    DISCONNECTED = auto()
    CONNECTING = auto()
    CONNECTED = auto()
    DISCONNECTING = auto()
    ERROR = auto()


class BaseDevice(ABC):
    """Base class for devices providing connection lifecycle management.

    Override notes:
    - Subclasses must implement get_state, get_capabilities, read, set.
    - Do not override connect/disconnect unless you must extend behavior;
      if you do, call super().connect()/disconnect() to preserve state.
    """

    def __init__(self, model: str, adapter: AdapterProtocol, config_loader: ConfigLoaderProtocol) -> None:
        self.model = model
        self.adapter: AdapterProtocol = adapter
        self.config_loader: ConfigLoaderProtocol = config_loader
        self._state: DeviceState = DeviceState.DISCONNECTED

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
            # Post-connect hook for subclasses
            on_connect = getattr(self, "_on_connect", None)
            if callable(on_connect):
                on_connect()
            self._state = DeviceState.CONNECTED
        except Exception as exc:
            self._state = DeviceState.ERROR
            raise ConnectionError(f"Connect error: {exc}") from exc

    def disconnect(self) -> None:
        if self._state is DeviceState.DISCONNECTED:
            return
        self._state = DeviceState.DISCONNECTING
        try:
            # Pre-disconnect hook for subclasses
            on_disconnect = getattr(self, "_on_disconnect", None)
            if callable(on_disconnect):
                on_disconnect()
            self.adapter.disconnect()
            self._state = DeviceState.DISCONNECTED
        except Exception as exc:
            self._state = DeviceState.ERROR
            raise ConnectionError(f"Disconnect error: {exc}") from exc

    def require_connected(self) -> None:
        if not self.is_connected:
            raise ConnectionError("Device is not connected")

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    @abstractmethod
    def get_state(self) -> str:
        ...

    @abstractmethod
    def get_capabilities(self) -> Dict[str, bool]:
        ...

    @abstractmethod
    def read(self, key: str) -> object:
        ...

    @abstractmethod
    def set(self, key: str, value: object) -> None:
        ...


    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} model={self.model!r} state={self._state.name}>"
