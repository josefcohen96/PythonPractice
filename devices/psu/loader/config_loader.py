from __future__ import annotations
from typing import Any, Dict
import os
import yaml

from devices.base import ConfigLoaderProtocol


class YamlPSUConfigLoader(ConfigLoaderProtocol):
    def __init__(self, base_dir: str | None = None) -> None:
        if base_dir is None:
            # default to devices/psu/config relative to this file
            base_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config")
        self.base_dir = base_dir
        self._capabilities_cache: Dict[str, Dict[str, bool]] = {}
        self._ranges_cache: Dict[str, Dict[str, Any]] = {}
        self._models_cache: list[Dict[str, Any]] | None = None

    def _load_yaml(self, filename: str) -> Any:
        path = os.path.join(self.base_dir, filename)
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def load_capabilities(self, model: str) -> Dict[str, bool]:
        if not self._capabilities_cache:
            data: Dict[str, Dict[str, bool]] = self._load_yaml("capabilities.yml")
            self._capabilities_cache = data or {}
        return dict(self._capabilities_cache.get(model, {}))

    def load_ranges(self, model: str) -> Dict[str, Any]:
        if not self._ranges_cache:
            data: Dict[str, Dict[str, Any]] = self._load_yaml("ranges.yml")
            self._ranges_cache = data or {}
        return dict(self._ranges_cache.get(model, {}))

    def load_model_info(self, model: str) -> Dict[str, Any]:
        if self._models_cache is None:
            data = self._load_yaml("models.yml")
            self._models_cache = data or []
        for entry in self._models_cache:
            if entry.get("model_id") == model:
                return dict(entry)
        return {}
