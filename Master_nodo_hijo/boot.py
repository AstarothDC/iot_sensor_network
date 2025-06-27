# boot.py – Nodo Hijo: Montaje SD y setup inicial
import os
from machine import SPI, Pin
import sdcard
import config

def mount_sd():
    try:
        spi = SPI(2, baudrate=1000000, polarity=0, phase=0,
                  sck=Pin(config.SD_SCK), mosi=Pin(config.SD_MOSI), miso=Pin(config.SD_MISO))
        sd = sdcard.SDCard(spi, Pin(config.SD_CS))
        os.mount(sd, "/sd")
        print("✅ SD montada en /sd")
        return True
    except Exception as e:
        print("❌ Error montando SD:", e)
        return False

# Ejecutar montaje al inicio
mount_sd()
