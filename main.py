"""Demonstration script for the instruments.

Runs a simple demo using the split device modules.
"""
from __future__ import annotations

from devices.signal_generator import SignalGenerator
from devices.spectrum_analyzer import SpectrumAnalyzer


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