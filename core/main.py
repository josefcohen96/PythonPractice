"""Demonstration script for the signal_lab project.

This script shows how to use the instrument classes defined in `devices.py`
using context managers to ensure clean resource management.  It sets a
frequency on a signal generator, enables its output, measures the frequency
with a spectrum analyzer, and then disables the output.  The printed output
illustrates the sequence of operations and the effect of simulated measurement
noise.
"""
import sys
import os

# Add the project root directory to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from __future__ import annotations
from devices.devices import SignalGenerator, SpectrumAnalyzer


def main() -> None:
    """Run the demonstration."""
    # Use nested context managers to manage multiple instruments
    with SignalGenerator(resource="GPIB0::10", min_freq=1e6, max_freq=1e9) as gen, \
         SpectrumAnalyzer(resource="GPIB0::20", accuracy_hz=5.0) as spec:
        # Set the desired frequency
        gen.frequency = 100e6  # 100 MHz
        gen.enable_output()
        # Measure the signal
        measured = spec.measure_frequency(gen)
        print(f"Main: The measured frequency is {measured:.2f} Hz")
        gen.disable_output()


if __name__ == "__main__":
    main()