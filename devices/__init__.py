"""Devices package.

Exports common demo instruments for convenience.

Note: Prefer importing specific modules (devices.signal_generator, devices.spectrum_analyzer).
"""

from .signal_generator import SignalGenerator  # noqa: F401
from .spectrum_analyzer import SpectrumAnalyzer  # noqa: F401
from .oven import Oven  # noqa: F401
