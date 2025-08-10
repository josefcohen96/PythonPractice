from typing import Literal

DeviceState = Literal["connected", "disconnected", "busy", "fault"]
ReadKey  = Literal["voltage", "current", "temp", "output"]
SetKey   = Literal["voltage", "current_limit", "output", "power"]
