from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional, Union
import yaml

from .loader.config_loader import PSUConfigLoader


class YamlPSUConfigLoader(PSUConfigLoader):
    """Load PSU configuration (capabilities, ranges, models) from YAML files.

    Expected files under base_dir:
      - capabilities.yml
      - ranges.yml
      - models.yml
    """

    def __init__(self, base_dir: Optional[Union[str, Path]] = None) -> None:
        if base_dir is None:
            # default to devices/psu/config directory
            base_dir = Path(__file__).resolve().parent / "config"
        self.base = Path(base_dir)
        self._cap = {}
        self._ranges = {}
        self._models = []
        self._load_all()

    def _load_yaml(self, name: str) -> object:
        p = self.base / name
        with p.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return data

    def _load_all(self) -> None:
        raw_cap = self._load_yaml("capabilities.yml") or {}
        raw_ranges = self._load_yaml("ranges.yml") or {}
        raw_models = self._load_yaml("models.yml") or []
        if not isinstance(raw_cap, dict):
            raise TypeError("capabilities.yml must map model -> capabilities")
        if not isinstance(raw_ranges, dict):
            raise TypeError("ranges.yml must map model -> ranges")
        if not isinstance(raw_models, list):
            raise TypeError("models.yml must be a list of model entries")
        self._cap = raw_cap
        self._ranges = raw_ranges
        self._models = raw_models

    # PSUConfigLoader API
    def load_capabilities(self, model: str) -> Dict[str, bool]:
        try:
            caps = self._cap[model]
        except KeyError as exc:
            raise KeyError(f"Capabilities for model '{model}' not found") from exc
        if not isinstance(caps, dict):
            raise TypeError("capabilities entry must be a dict")
        # Coerce values to bool
        return {k: bool(v) for k, v in caps.items()}

    def load_ranges(self, model: str) -> Dict[str, Union[float, str]]:
        try:
            rng = self._ranges[model]
        except KeyError as exc:
            raise KeyError(f"Ranges for model '{model}' not found") from exc
        if not isinstance(rng, dict):
            raise TypeError("ranges entry must be a dict")
        return rng

    def load_model_info(self, model: str) -> Dict[str, object]:
        for entry in self._models:
            if entry.get("model_id") == model:
                return dict(entry)
        raise KeyError(f"Model info for '{model}' not found")
