from __future__ import annotations
import warnings
from .strategies import PsuStrategy, PSUContext, VirtualPsuStrategy, RealPsuStrategy

warnings.warn(
    "devices.psu.strategy module is deprecated; use devices.psu.strategies.*",
    DeprecationWarning,
    stacklevel=2,
)

__all__ = [
    "PsuStrategy",
    "PSUContext",
    "VirtualPsuStrategy",
    "RealPsuStrategy",
]
