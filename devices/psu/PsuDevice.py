
from devices.base import BaseDevice
from core.exceptions import ValueError
from typing import Any, Dict
import os
import sys

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)


class PSU(BaseDevice):

    def __init__(self, model: str, adapter: Any, config_loader: Any) -> None:

        self._listActions = ["voltage", "current", "temp", "output"]
        if adapter is None:
            raise ValueError("adapter is required")
        if not model:
            raise ValueError("model is required")
        if config_loader is None:
            raise ValueError("config loader is required")

        super().__init__(model, adapter, config_loader)
        self.type = "psu"

        try:
            self._capabilities = self.config_loader.load_capabilities(
                self.model)
            self._ranges = self.config_loader.load_ranges(self.model)
            self._state = "disconnected"  # initiate state

        finally:
            pass

    def connect(self) -> bool:
        result = self.adapter.connect()
        if result == "success":
            self._state = "connected"
            return True
        self._state = "disconnected"
        return False

    def disconnect(self) -> None:
        result = self.adapter.disconnect()

        if result == "success":
            self._state = "connected"
            return True

        self._state = "disconnected"
        return False

    def get_state(self) -> str:
        return self._state

    def get_capabilities(self) -> Dict[str, bool]:
        return self._capabilities

    def read(self, key: str) -> None:
        if key not in self._listActions:
            return f"unable to read {key} from {self._listActions}"
        
        

    def set(self, key: str, value: Any) -> Any:
        pass
