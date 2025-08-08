# Contracts – חוזה למימוש רכיבים

## מתודות חובה בכל דרייבר
- async connect() -> None
- async disconnect() -> None
- async capabilities() -> List[str]
- async state() -> str          # "connected" / "disconnected" / "busy" / "fault"
- async read(key: str) -> Any
- async set(key: str, value: Any) -> None
- meta() -> Dict[str, Any]       # מידע נוסף: model, vendor, firmware...

## חוקים
- כל מפתח ב-read/set חייב להופיע ב-capabilities הרלוונטי.
- כל set(key, value) חייב לבצע ולידציה מול ranges (לפי דגם).
- כל read(key) חייב להחזיר ערך חוקי או להרים חריגה מוגדרת.

## חריגות
- אם קריאה ל-read/set לא נתמכת: CapabilityMissing
- אם ערך חורג מטווח: OutOfRange
- אם הרכיב לא מגיב בזמן: DeviceTimeout
- אם הרכיב במצב שאינו מאפשר פעולה: DeviceBusy
- אם יש שגיאת פרוטוקול/נתונים: ProtocolError

## יחידות סטנדרטיות
- temp: °C
- voltage: V
- current: A
- freq: Hz
- amp_dbm: dBm
- sample_rate: sps
- amplitude_vpp: Vpp
