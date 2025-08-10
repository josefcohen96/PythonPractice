
from typing import Any, Dict
import os
import sys

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from devices.base import BaseDevice, DeviceState


class PSU(BaseDevice):

    def __init__(self, model: str, adapter: Any, config_loader: Any) -> None:

        self._listActions = ["voltage", "current", "temp"]
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
            # base starts as DISCONNECTED
        finally:
            pass

    def connect(self) -> None:
        super().connect()

    def disconnect(self) -> None:
        super().disconnect()

    def get_state(self) -> str:
        return self.state.name.lower()

    def get_capabilities(self) -> Dict[str, bool]:
        return self._capabilities

    def read(self, key: str) -> None:
        self.require_connected()
        if key not in self._listActions:
            return f"unable to read {key} from {self._listActions}"

    def set(self, key: str, value: Any) -> Any:
        self.require_connected()
        pass
