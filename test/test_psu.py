from __future__ import annotations

import os
import sys
from unittest import loader
import pytest

# הוספת ספריית הפרויקט ל-PYTHONPATH כדי שמודול devices יימצא
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")))


from core.exceptions import ConnectionError
from devices.psu.adapters.sim_adapter import SimAdapter
from devices.psu.yaml_config_loader import YamlPSUConfigLoader
from devices.psu.strategy import VirtualPsuStrategy
from devices.psu.PsuDevice import PSU



def test_virtual_psu_flow():
    """
    וידוא ש-PSU וירטואלי מתחבר, מבצע פעולות, ומחזיר ערכים לא שליליים.
    """
    loader = YamlPSUConfigLoader()
    print("#############################")
    print("Capabilities:", loader.load_capabilities("RIGOL-DP832"))
    print("Ranges:", loader.load_ranges("RIGOL-DP832"))
    print("#############################")
    psu = PSU(
        model="RIGOL-DP832",
        adapter=SimAdapter(),
        config_loader=loader,
        strategy=VirtualPsuStrategy(),
    )

    # ניסיון קריאה לפני connect אמור לזרוק ConnectionError
    with pytest.raises(ConnectionError):
        psu.read("voltage")

    psu.connect()
    assert psu.get_state() == "connected"

    # הגדרת מתח, הגבלת זרם והפעלת יציאה
    psu.set("voltage", 5.0)
    psu.set("current_limit", 0.2)
    psu.set("output", True)

    v = psu.read("voltage")
    t = psu.read("temp")
    i = psu.read("current")
    out = psu.read("output")

    # i = psu.read("current")

    # בדיקות בסיסיות: מתח וזרם אי-שליליים, טמפרטורה float/None, מצב יציאה בוליאני
    assert v >= 0.0
    # assert i >= 0.0
    assert isinstance(t, float) or t is None
    assert i >= 0.0
    assert isinstance(out, bool)

    psu.disconnect()
    assert psu.get_state() == "disconnected"
