# rtc_ds1307.py – Módulo para manejar RTC DS1307 o DS3231 vía I2C

from machine import I2C, Pin
import ds1307
import config

class RTC_DS1307:
    def __init__(self, i2c):
        self.rtc = ds1307.DS1307(i2c)

    def get_timestamp(self):
        y, m, d, wd, h, mi, s = self.rtc.datetime()
        return "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}".format(y, m, d, h, mi, s)

    def set_time(self, y, m, d, h, mi, s):
        self.rtc.datetime((y, m, d, 0, h, mi, s, 0))

    def set_time_from_string(self, timestr):
        """
        Recibe un string ISO 8601 (ej. '2025-06-28T14:25:00') y configura el RTC.
        """
        try:
            date_part, time_part = timestr.strip().split("T")
            year, month, day = [int(x) for x in date_part.split("-")]
            hour, minute, second = [int(x) for x in time_part.split(":")]
            self.set_time(year, month, day, hour, minute, second)
            print("✅ RTC actualizado:", self.get_timestamp())
        except Exception as e:
            print("❌ Error configurando RTC:", e)

def setup_rtc():
    i2c = I2C(1, scl=Pin(config.I2C_SCL), sda=Pin(config.I2C_SDA))
    return RTC_DS1307(i2c)

    
