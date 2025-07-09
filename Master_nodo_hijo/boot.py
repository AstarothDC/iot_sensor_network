# boot.py – Nodo Hijo: Montaje de SD y preparación del RTC

import os
import time
from machine import SPI, Pin, I2C
import sdcard
import config
import network
import ntptime
import ds1307

def mount_sd():
    print("[BOOT] Montando SD...")
    try:
        spi = SPI(2, baudrate=1000000, polarity=0, phase=0,
                  sck=Pin(config.SPI_SCK),
                  mosi=Pin(config.SPI_MOSI),
                  miso=Pin(config.SPI_MISO))
        sd = sdcard.SDCard(spi, Pin(config.SD_CS))
        os.mount(sd, "/sd")
        print("✅ SD montada en /sd. Archivos:", os.listdir("/sd"))
        return True
    except Exception as e:
        print("❌ Error montando SD:", e)
        return False

def sync_rtc():
    print("🕒 Sincronizando RTC desde nodo hijo...")
    i2c = I2C(0, scl=Pin(config.I2C_SCL), sda=Pin(config.I2C_SDA))
    ds = ds1307.DS1307(i2c)
    rtc = machine.RTC()

    wlan = network.WLAN(network.STA_IF)
    if wlan.isconnected():
        try:
            print("🌐 Obteniendo hora por NTP...")
            ntptime.settime()
            utc_time = time.localtime(time.time() + config.TIMEZONE_OFFSET)
            rtc.datetime((utc_time[0], utc_time[1], utc_time[2], utc_time[6],
                          utc_time[3], utc_time[4], utc_time[5], 0))
            ds.datetime((utc_time[0], utc_time[1], utc_time[2], utc_time[6],
                         utc_time[3], utc_time[4], utc_time[5]))
            print("✅ RTC sincronizado por NTP:", utc_time)
        except Exception as e:
            print("⚠️ Fallo en NTP. Intentando cargar hora desde RTC DS1307...")
            try:
                rtc_time = ds.datetime()
                rtc.datetime((rtc_time[0], rtc_time[1], rtc_time[2], rtc_time[6],
                              rtc_time[3], rtc_time[4], rtc_time[5], 0))
                print("✅ Hora cargada desde RTC:", rtc_time)
            except Exception as e:
                print("❌ No se pudo cargar hora del RTC:", e)
    else:
        print("📡 Sin Wi-Fi. Se usará hora RTC local (si disponible).")

# === Ejecutar procesos iniciales ===
mount_sd()
sync_rtc()
print("✅ Finalizó boot.py – ejecutando main.py...\n")
time.sleep(1)

