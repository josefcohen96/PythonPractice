"""Oven device (demo)."""

from __future__ import annotations

from typing import Optional

from core.exceptions import ConnectionError, RangeError


class Oven:
    """Simple oven abstraction for temperature control.

    Override notes:
    - For real IO, ensure __enter__/__exit__ manage transport correctly.
    - Raise exceptions instead of returning them from setters.
    """

    def __init__(self, resource: str, minTemp: float, maxTemp: float, connection: bool) -> None:
        self._temp: Optional[float] = None
        self.resource = resource
        self.minTemp = minTemp
        self.maxTemp = maxTemp
        self._connection = connection

    @property
    def temp(self) -> Optional[float]:
        return self._temp

    @temp.setter
    def temp(self, value: float) -> None:
        if not self._connection:
            raise ConnectionError("oven is not connected")
        if value < self.minTemp or value > self.maxTemp:
            raise RangeError(f"value: {value} is not in range, range is: [{self.minTemp}, {self.maxTemp}]")
        self._temp = value

    def __enter__(self) -> "Oven":
        self._connection = True
        print("[Oven] Connected")
        return self

    def __exit__(self, exec_stype, exec_) -> None:
        if self._connection:
            self._connection = False
            print("[Oven] Disconnected")
