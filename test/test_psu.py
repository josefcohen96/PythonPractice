from __future__ import annotations

import pytest

from devices.psu import PSU, VirtualPsuStrategy
from devices.psu.yaml_config_loader import YamlPSUConfigLoader
from devices.psu.adapters.sim_adapter import SimAdapter


def test_psu_virtual_basic_flow():
    loader = YamlPSUConfigLoader()
    psu = PSU(model="RIGOL-DP832", adapter=SimAdapter(), config_loader=loader, strategy=VirtualPsuStrategy())
    with pytest.raises(Exception):
        # not connected yet
        psu.read("voltage")

    psu.connect()
    psu.set("voltage", 3.3)
    psu.set("current_limit", 0.1)
    psu.set("output", True)
    v = psu.read("voltage")
    assert v >= 0
    psu.set("power_cycle", None)
    assert isinstance(psu.read("output"), bool)
    psu.disconnect()
