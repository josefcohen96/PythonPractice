from __future__ import annotations

import pytest

from devices.psu.PsuDevice import PSU
from devices.psu.strategy import VirtualPsuStrategy
from devices.psu.yaml_config_loader import YamlPSUConfigLoader
from devices.psu.adapters.sim_adapter import SimAdapter


def test_psu_virtual_basic_flow():
    loader = YamlPSUConfigLoader()
    psu = PSU(model="RIGOL-DP832", adapter=SimAdapter(), config_loader=loader, strategy=VirtualPsuStrategy())
    with pytest.raises(ConnectionError):
        psu.read("voltage")

    # connect the device
    psu.connect()
    assert psu.get_state() == "connected"

    # set voltage, current limit and enable output
    psu.set("voltage", 5.0)
    psu.set("current_limit", 0.2)
    psu.set("output", True)

    # read back simulated measurements
    v = psu.read("voltage")
    i = psu.read("current")
    t = psu.read("temp")
    out = psu.read("output")

    # voltage/current should be non‑negative floats, temp a float or None if unsupported
    assert v >= 0.0
    assert i >= 0.0
    assert isinstance(t, float) or t is None
    assert isinstance(out, bool)

    # perform a power cycle; output remains a boolean afterwards
    psu.set("power_cycle", None)
    assert isinstance(psu.read("output"), bool)

    # disconnect
    psu.disconnect()
    assert psu.get_state() == "disconnected"