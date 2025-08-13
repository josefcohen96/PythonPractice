# test/test_psu_cm.py
from __future__ import annotations

import os
import pytest
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from core.exceptions import ConnectionError
from adapters.psu import SimAdapter
from devices.psu.yaml_config_loader import YamlPSUConfigLoader
from devices.psu.strategy import VirtualPsuStrategy, RealPsuStrategy
from devices.psu.PsuDevice import PSU

try:
    from adapters.telnet_adapter import TelnetAdapter
    HAS_TELNET = True
except Exception:
    HAS_TELNET = False

try:
    from adapters.ssh_adapter import SSHAdapter
    HAS_SSH = True
except Exception:
    HAS_SSH = False


@pytest.fixture(scope="module")
def loader() -> YamlPSUConfigLoader:
    return YamlPSUConfigLoader()


@pytest.mark.parametrize("strategy", [
    VirtualPsuStrategy(),
    RealPsuStrategy(),   # כרגע מממש ע"י mirror ל־Virtual; עדיין טוב לכסות API
])
@pytest.mark.parametrize("adapter", [
    SimAdapter(),  # תמיד זמין
    pytest.param(
        TelnetAdapter(host=os.getenv("PSU_TELNET_HOST", "127.0.0.1"), port=int(os.getenv("PSU_TELNET_PORT", "23"))),
        marks=pytest.mark.skipif(not HAS_TELNET or not os.getenv("PSU_TELNET_HOST"),
                                 reason="TelnetAdapter not available or no PSU_TELNET_HOST set")
    ),
    pytest.param(
        SSHAdapter(host=os.getenv("PSU_SSH_HOST", ""), username=os.getenv("PSU_SSH_USER", "user"),
                   password=os.getenv("PSU_SSH_PASS", "pass"), port=int(os.getenv("PSU_SSH_PORT", "22"))),
        marks=pytest.mark.skipif(not HAS_SSH or not os.getenv("PSU_SSH_HOST"),
                                 reason="SSHAdapter not available or no PSU_SSH_HOST set")
    ),
])
def test_psu_flow_with_context(loader, adapter, strategy):
    """
    Using 'with PSU(...) as psu:' so connect/disconnect happen automatically.
    """
    model = "RIGOL-DP832"

    # לפני connect — קריאה אמורה לזרוק ConnectionError
    psu_cold = PSU(model=model, adapter=SimAdapter(), config_loader=loader, strategy=strategy)
    with pytest.raises(ConnectionError):
        psu_cold.read("voltage")

    # using context manager 
    with PSU(model=model, adapter=adapter, config_loader=loader, strategy=strategy) as psu:
        # הדפסה/וידוא קונפיג
        caps = psu.get_capabilities()
        ranges = loader.load_ranges(model)
        assert isinstance(caps, dict) and "set_voltage" in caps
        assert "voltage" in ranges and "min" in ranges["voltage"] and "max" in ranges["voltage"]

        # פעולות בסיסיות
        psu.set("voltage", 5.0)
        psu.set("current_limit", 0.2)
        psu.set("output", True)

        v = psu.read("voltage")
        i = psu.read("current")
        t = psu.read("temp")
        out = psu.read("output")

        assert v >= 0.0
        assert i >= 0.0
        assert isinstance(t, float) or t is None
        assert isinstance(out, bool)

    # מחוץ ל־with — כבר נותק; כל פעולה שדורשת חיבור צריכה להיכשל
    with pytest.raises(ConnectionError):
        psu_cold.require_connected()  # הדגמה: מופע אחר שלא חובר
    # המופע שהיה בתוך ה-with יצא מהתחום, אבל אם שמרת רפרנס, גם עליו read צריך לזרוק


def test_psu_context_manager_closes_on_exception(loader):
    """
    מוודא שגם כשזורקים חריגה בתוך הבלוק, ה־__exit__ מנתק.
    """
    model = "RIGOL-DP832"
    psu_ref = None
    try:
        with PSU(model=model, adapter=SimAdapter(), config_loader=loader, strategy=VirtualPsuStrategy()) as psu:
            psu_ref = psu
            psu.set("output", True)
            # זורקים חריגה כדי לבדוק שפונקציית __exit__ רצה ומנתקת
            raise RuntimeError("boom")
    except RuntimeError:
        pass

    # כעת psu_ref אמור להיות מנותק (אם שמרנו רפרנס)
    # קריאה שדורשת חיבור אמורה להיכשל
    if psu_ref is not None:
        with pytest.raises(ConnectionError):
            psu_ref.read("voltage")
