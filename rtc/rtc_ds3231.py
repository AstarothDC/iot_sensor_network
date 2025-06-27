# rtc_ds3231.py – Manejo del módulo de reloj DS3231

import ds3231

def get_timestamp(i2c):
    try:
        rtc = ds3231.DS3231(i2c)
        y, m, d, wd, h, mi, s = rtc.get_time()
        return "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}".format(y, m, d, h, mi, s)
    except Exception as e:
        print("Error leyendo DS3231:", e)
        return "0000-00-00T00:00:00"