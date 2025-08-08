# PSU Driver API

## read(key: str)
- voltage → V
- current → A
- temp → °C
- output → bool

## set(key: str, value: Any)
- voltage: float, 0..maxV
- current_limit: float, 0..maxA
- output: bool
- power_cycle: None

## state()
- connected/disconnected/busy/fault

## capabilities()
- מחזיר את רשימת המפתחות הנתמכים לפי capabilities.yml

## התנהגות busy:
- power_cycle → busy ל־5 שניות
- set_voltage → busy ל־100ms
