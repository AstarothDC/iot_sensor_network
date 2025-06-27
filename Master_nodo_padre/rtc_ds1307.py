# rtc_ds1307.py – Módulo para manejar RTC DS1307 o DS3231 vía I2C

from machine import I2C
import ds1307

class RTC_DS1307:
    def __init__(self, i2c):
        self.rtc = ds1307.DS1307(i2c)

    def get_timestamp(self):
        y, m, d, wd, h, mi, s = self.rtc.datetime()
        return "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}".format(y, m, d, h, mi, s)

    def set_time(self, y, m, d, h, mi, s):
        self.rtc.datetime((y, m, d, 0, h, mi, s, 0))
