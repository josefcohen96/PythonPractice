 # PSU Validators

## חוקים:
1. שינוי מתח (set_voltage) כשה-output פעיל מעל 10% מהטווח → זרוק אזהרת Ramp.
2. ערך זרם (set_current_limit) מעל המקסימום → זרוק OutOfRange.
3. אם הרכיב במצב busy → זרוק DeviceBusy על כל פעולת set.
4. שינוי output ל-on דורש לפחות 500ms השהייה בין פקודות.
