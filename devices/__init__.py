"""Devices package.

Exports common demo instruments for convenience.

Note: Prefer importing specific modules (devices.psu, ...).
"""
from . import psu as psu  # make `devices.psu` available via package import
from .psu import PSU, PsuStrategy, VirtualPsuStrategy  # noqa: F401

# Try to expose RealPsuStrategy only if it exists
try:
    from .psu import RealPsuStrategy  # noqa: F401
    __all__ = ["psu", "PSU", "PsuStrategy", "VirtualPsuStrategy", "RealPsuStrategy"]
except Exception:
    __all__ = ["psu", "PSU", "PsuStrategy", "VirtualPsuStrategy"]
