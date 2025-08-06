"""Example tests for the signal_lab instruments.

These tests use the pytest framework to verify the behaviour of the
SignalGenerator and SpectrumAnalyzer classes.  They check that valid
frequencies can be set, invalid frequencies raise errors, and that the
spectrum analyzer measures frequencies within the specified accuracy.

Note: This file is not executed automatically in this environment because
pytest is not installed.  It is provided for completeness and as an example
of good testing practices.
"""

import pytest

from devices import SignalGenerator, SpectrumAnalyzer
from exceptions import RangeError, InstrumentError


@pytest.fixture
def sig_gen() -> SignalGenerator:
    return SignalGenerator(min_freq=1e6, max_freq=1e9)


@pytest.fixture
def spec_analyzer() -> SpectrumAnalyzer:
    return SpectrumAnalyzer(accuracy_hz=5.0)


@pytest.mark.parametrize("freq", [1e6, 10e6, 500e6])
def test_set_valid_frequency(sig_gen: SignalGenerator, freq: float) -> None:
    with sig_gen:
        sig_gen.frequency = freq
        assert sig_gen.frequency == freq


@pytest.mark.parametrize("freq", [0.5e6, 2e9])
def test_set_invalid_frequency_raises(sig_gen: SignalGenerator, freq: float) -> None:
    with sig_gen:
        with pytest.raises(RangeError):
            sig_gen.frequency = freq


def test_measure_frequency_within_accuracy(sig_gen: SignalGenerator, spec_analyzer: SpectrumAnalyzer) -> None:
    target_freq = 100e6
    with sig_gen, spec_analyzer:
        sig_gen.frequency = target_freq
        sig_gen.enable_output()
        measured = spec_analyzer.measure_frequency(sig_gen)
        assert abs(measured - target_freq) <= spec_analyzer.accuracy_hz
        sig_gen.disable_output()


def test_measure_frequency_without_setting_raises(spec_analyzer: SpectrumAnalyzer) -> None:
    gen = SignalGenerator()
    with gen, spec_analyzer:
        with pytest.raises(InstrumentError):
            spec_analyzer.measure_frequency(gen)