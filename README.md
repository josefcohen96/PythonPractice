# Signal Lab Demo Project

This is a simple demo project that illustrates how to design a small Python
codebase around test‑equipment classes and how to write clean, testable code.

The goal of the project is to model a **signal generator** and a **spectrum
analyzer**, provide a clean API for interacting with them, and demonstrate
good practices such as using context managers for resource management and
property setters/getters for encapsulation.  We also include a small set of
tests to show how you might validate your code using `pytest`.

## Structure

```
.
├── core/                  # Custom exceptions
├── devices/
│   ├── base/              # BaseDevice, protocols
│   ├── psu/               # PSU device, strategies, YAML contracts
│   ├── signal_generator.py
│   ├── spectrum_analyzer.py
│   └── oven.py
├── adapters/              # Transport adapters (ssh/telnet)
├── examples/              # Small runnable demos
├── test/                  # Pytest test suite
├── pyproject.toml         # Editable install metadata
├── requirements.txt
└── README.md
```

## Running the example

You can run the example script directly with Python to see how the classes
operate together:

Windows PowerShell:

```
pip install -e .
python .\main.py
```

This script demonstrates opening both instruments via `with` statements,
setting a frequency on the signal generator, measuring it with the
spectrum analyzer, and printing the results.

## Running the tests

The test file is written using `pytest`. If you have pytest installed, you
can run the tests with:

```
pytest -q
```

If `pytest` is not available, the tests will not run; however, the code is
structured to be self‑contained and easy to convert to `unittest` if
necessary.