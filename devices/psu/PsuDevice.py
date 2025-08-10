from typing import Any, Dict
import os
import sys

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from devices.base import BaseDevice
from core.exceptions import CapabilityMissing, RangeError


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

        self._capabilities = self.config_loader.load_capabilities(self.model)
        self._ranges = self.config_loader.load_ranges(self.model)
        self._settings: Dict[str, Any] = {}

    def connect(self) -> None:
        super().connect()

    def disconnect(self) -> None:
        super().disconnect()

    def get_state(self) -> str:
        return self.state.name.lower()

    def get_capabilities(self) -> Dict[str, bool]:
        return self._capabilities

    def _require_capability(self, name: str) -> None:
        if not self._capabilities.get(name, False):
            raise CapabilityMissing(f"Capability '{name}' is not available for model {self.model}")

    def _require_in_range(self, key: str, value: float) -> None:
        rng = self._ranges.get(key)
        if not rng:
            return
        min_v = rng.get("min")
        max_v = rng.get("max")
        if min_v is not None and value < min_v:
            raise RangeError(f"{key} {value} is below minimum {min_v}")
        if max_v is not None and value > max_v:
            raise RangeError(f"{key} {value} is above maximum {max_v}")

    def read(self, key: str) -> Any:
        self.require_connected()
        if key not in self._listActions:
            return f"unable to read {key} from {self._listActions}"

        # Prefer adapter methods if available, else return cached setting
        method_name = f"read_{key}"
        if hasattr(self.adapter, method_name):
            return getattr(self.adapter, method_name)()
        return self._settings.get(key)

    def set(self, key: str, value: Any) -> Any:
        self.require_connected()
        if key == "voltage":
            self._require_capability("set_voltage")
            self._require_in_range("voltage", float(value))
            if hasattr(self.adapter, "set_voltage"):
                getattr(self.adapter, "set_voltage")(float(value))
            self._settings["voltage"] = float(value)
            return None

        if key == "current_limit":
            self._require_capability("set_current_limit")
            self._require_in_range("current", float(value))
            if hasattr(self.adapter, "set_current_limit"):
                getattr(self.adapter, "set_current_limit")(float(value))
            self._settings["current_limit"] = float(value)
            return None

        if key == "output":
            self._require_capability("toggle_output")
            on = bool(value)
            if on and hasattr(self.adapter, "output_on"):
                self.adapter.output_on()
            elif not on and hasattr(self.adapter, "output_off"):
                self.adapter.output_off()
            self._settings["output"] = on
            return None

        return f"unsupported set key: {key}"

    # Optional convenience methods
    def output_on(self) -> None:
        self.set("output", True)

    def output_off(self) -> None:
        self.set("output", False)