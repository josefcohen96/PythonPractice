
from typing import Any, Dict
import os
import sys

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from devices.psu.adapters.interface import PSUAdapterInterface
from core.exceptions import ValueError, CapabilityMissing, DeviceError, DeviceTimeout, ProtocolError
from devices.base import BaseDevice
from devices.psu.loader.config_loader import PSUConfigLoader


class PSU(BaseDevice):

    def __init__(self, model: str, adapter: PSUAdapterInterface, config_loader: PSUConfigLoader) -> None:

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
            self._state = "disconnected"  # initiate state

        finally:
            pass

    def connect(self) -> None:
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

    def read(self, key: str) -> int:
        try:
            idx = self._listActions.index(key)
            if idx == 1:
                value = self._read_voltage()
            elif idx == 2:
                value = self._read_current()

            else:
                value = self._read_temp()

            return {key: value}


        except ValueError: # key wasnot found
            return ValueError(" key was not found")

        
        
    def set(self, key: str, value: Any) -> Any:
        pass


    def _read_voltage(self) -> float:
        # 1. בדיקת יכולת
        if not self._capabilities.get("read_voltage", False):
            raise CapabilityMissing("read_voltage capability is not available for this PSU")

        # 2. בדיקת חיבור
        if self._state == "disconnected":
            raise DeviceError("PSU is disconnected")

        # 3. ביצוע קריאה מה-adapter
        try:
            value = self.adapter.read_voltage()
        except TimeoutError as e:
            raise DeviceTimeout("Timeout while reading voltage") from e
        except Exception as e:
            raise ProtocolError("Protocol error while reading voltage") from e

        # 4. עדכון סטינגס ומצב
        self._settings["voltage"] = value

        return value