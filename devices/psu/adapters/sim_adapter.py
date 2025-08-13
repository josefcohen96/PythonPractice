from __future__ import annotations
import warnings
from adapters.psu import SimAdapter as SimAdapter  # re-export

warnings.warn(
    "devices.psu.adapters.sim_adapter.SimAdapter is deprecated; use adapters.psu.SimAdapter",
    DeprecationWarning,
    stacklevel=2,
)