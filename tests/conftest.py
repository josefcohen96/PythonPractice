from __future__ import annotations

import dataclasses
from typing import Any, Dict, Tuple, Protocol

import pytest

from core.exceptions import ConnectionError
from devices.psu.PsuDevice import PSU
from devices.psu.strategy import VirtualPsuStrategy, RealPsuStrategy
from devices.psu.yaml_config_loader import YamlPSUConfigLoader
from devices.psu.adapters import SimAdapter


class DriverProtocol(Protocol):
    def open(self) -> None: ...
    def close(self) -> None: ...
    def write(self, data: bytes) -> None: ...
    def query(self, data: bytes) -> bytes: ...


class FakeTcpDriver:
    def __init__(self, scripted: Dict[bytes, bytes] | None = None) -> None:
        self.scripted: Dict[bytes, bytes] = scripted or {}
        self.opened: bool = False

    def open(self) -> None:
        self.opened = True

    def close(self) -> None:
        self.opened = False

    def write(self, data: bytes) -> None:
        if not self.opened:
            raise ConnectionError("driver not open")
        # side-effect only; no response

    def query(self, data: bytes) -> bytes:
        if not self.opened:
            raise ConnectionError("driver not open")
        try:
            return self.scripted[data]
        except KeyError:
            return b""


class ScpiLikeAdapter:
    """A minimal SCPI-like adapter over a byte-oriented driver.

    Provides a subset API used by the example tests.
    """

    def __init__(self, driver: FakeTcpDriver) -> None:
        self._driver = driver

    def connect(self) -> None:
        self._driver.open()

    def disconnect(self) -> None:
        self._driver.close()

    def is_connected(self) -> bool:
        return self._driver.opened

    # Example convenience methods used in tests
    def set_voltage(self, v: float) -> None:
        self._driver.write(f"VOLT {v}\n".encode("ascii"))

    def set_current_limit(self, a: float) -> None:
        self._driver.write(f"CURR {a}\n".encode("ascii"))

    def set_output(self, on: bool) -> None:
        self._driver.write(("OUTP ON\n" if on else "OUTP OFF\n").encode("ascii"))

    def measure_voltage(self) -> float:
        resp = self._driver.query(b"MEAS:VOLT?")
        return float(resp.decode("ascii").strip()) if resp else 0.0

    def measure_current(self) -> float:
        resp = self._driver.query(b"MEAS:CURR?")
        return float(resp.decode("ascii").strip()) if resp else 0.0


@dataclasses.dataclass(frozen=True)
class PsuVariant:
    name: str
    strategy: Any
    adapter_factory: Any


def build_psu_from_variant(variant: PsuVariant) -> Tuple[PSU, Any]:
    loader = YamlPSUConfigLoader()
    adapter = variant.adapter_factory()
    psu = PSU(model="RIGOL-DP832", adapter=adapter, config_loader=loader, strategy=variant.strategy)
    return psu, adapter


@pytest.fixture(scope="module")
def PSU_VARIANTS() -> Tuple[PsuVariant, PsuVariant, PsuVariant]:
    return (
        PsuVariant(name="sim+virtual", strategy=VirtualPsuStrategy(), adapter_factory=lambda: SimAdapter()),
        PsuVariant(name="sim+real", strategy=RealPsuStrategy(), adapter_factory=lambda: SimAdapter()),
        PsuVariant(name="sim+virtual-delayed", strategy=VirtualPsuStrategy(), adapter_factory=lambda: SimAdapter(connect_delay_s=0.05)),
    )