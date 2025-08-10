# Architecture Overview

- devices/
  - base/: Core contracts and base behavior (stateful connect/disconnect)
  - psu/: PSU device and its adapters
  - devices.py: Demo instruments (SignalGenerator, SpectrumAnalyzer, Oven)
- core/
  - exceptions.py: Unified exception types
- test/: Pytest-based tests

Key contracts
- AdapterProtocol: connect(), disconnect(), is_connected()
- ConfigLoaderProtocol: load_capabilities(model), load_ranges(model)
- BaseDevice: owns state machine (CONNECTING, CONNECTED, etc.) and guards

Scalability
- Add new devices by subclassing BaseDevice and using the same adapter/config loader contracts
- Add new transports by implementing AdapterProtocol (e.g., Telnet, SSH, VISA)
- Share adapters across devices when the transport is generic
- Keep operations device-focused (validation, ranges, SCPI) while BaseDevice manages state

Conventions
- Methods raise exceptions on failure rather than returning bools
- connect()/disconnect() are idempotent
- Avoid shadowing built-in exceptions; use core.exceptions.*