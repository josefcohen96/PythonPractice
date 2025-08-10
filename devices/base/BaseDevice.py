from abc import ABC, abstractmethod
from typing import Any, Dict
from enum import Enum, auto
from core.exceptions import ConnectionError


class DeviceState(Enum):
    DISCONNECTED = auto()
    CONNECTED = auto()
    ERROR = auto()


class BaseDevice(ABC):
    def __init__(self, model: str, adapter: Any, config_loader: Any) -> None:
        self.model = model
        self.adapter = adapter
        self.config_loader = config_loader
        self._state = DeviceState.DISCONNECTED

    @property
    def state(self) -> DeviceState:
        return self._state

    @property
    def is_connected(self) -> bool:
        return self._state is DeviceState.CONNECTED  # return true if connected

    @abstractmethod
    def connect(self) -> None:
        if self.is_connected:
            return
        try:
            self.adapter.connect()

            self._state = DeviceState.CONNECTED

        except Exception as exc:
            raise ConnectionError(f" connect error with {exc}")

    @abstractmethod
    def disconnect(self) -> None:
        if not self._state:
            return

        try:
            self.adapter.disconnect()
            self._state = DeviceState.DISCONNECTED

        except Exception as exc:
            return ConnectionError(f"disconnect with error: {exc}")

    @abstractmethod
    def get_state(self) -> str:
        pass

    @abstractmethod
    def get_capabilities(self) -> Dict[str, bool]:
        pass

    @abstractmethod
    def read(self, key: str) -> {}:
        pass

    @abstractmethod
    def set(self, key: str, value: Any) -> Any:
        pass
