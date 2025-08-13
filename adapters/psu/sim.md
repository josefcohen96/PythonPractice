# PSU Simulator Adapter

## קריאות read:
- voltage: ערך נשמר בזיכרון (ברירת מחדל 0)
- current: תמיד 0.1 * voltage
- temp: קבוע 25°C

## פעולות set:
- set_voltage: משנה את voltage בזיכרון
- toggle_output: on/off משפיע על קריאות voltage/current

## Fault Injection:
- ניתן לקבוע flag "no_response" שיגרום לכל פעולה לזרוק DeviceTimeout