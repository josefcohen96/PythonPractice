from abc import ABC, abstractmethod
from typing import Any, Dict

class PSUConfigLoader(ABC):
    """
    Abstract interface for loading PSU model configuration data.

    Implementations of this loader are responsible for providing
    model-specific configuration details from a given source
    (e.g., YAML files, JSON, database, API).

    This includes:
        • Capabilities — which features the PSU supports
          (e.g., can read voltage, can set current limit, supports power cycling).
        • Ranges — valid operating ranges for adjustable parameters
          (e.g., voltage min/max, current limit min/max).
        • Model info — general descriptive metadata about the PSU model
          (e.g., manufacturer, model name, communication protocol).

    All methods take the PSU model name as input and return the
    corresponding configuration data in a structured form.
    """
    @abstractmethod
    def load_capabilities(self, model: str) -> Dict[str, bool]:
        """Return a dictionary of capability flags for the given model."""
        pass

    @abstractmethod
    def load_ranges(self, model: str) -> Dict[str, Dict[str, float | str]]:
        """Return a dictionary mapping parameter names to their allowed ranges."""
        pass

    @abstractmethod
    def load_model_info(self, model: str) -> Dict[str, Any]:
        """Return general metadata about the given PSU model."""
        pass
