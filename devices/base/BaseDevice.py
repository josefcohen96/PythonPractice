from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseDevice(ABC):
    def __init__(self, model: str, adapter: Any, config_loader: Any) -> None:
        self.model = model
        self.adapter = adapter
        self.config_loader = config_loader
        self.state = ""
    @abstractmethod
    def connect(self) -> bool:
        pass

    @abstractmethod
    def disconnect(self) -> None:
        pass

    @abstractmethod
    def get_state(self) -> str:
        pass

    @abstractmethod
    def get_capabilities(self) -> Dict[str, bool]:
        pass

    @abstractmethod
    def read(self, key: str) -> None:
        pass

    @abstractmethod
    def set(self, key: str, value: Any) -> Any:
        pass
