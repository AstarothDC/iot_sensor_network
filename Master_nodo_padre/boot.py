# boot.py – Configuración inicial del nodo (montaje de microSD)

from machine import SPI, Pin
import os
import sdcard
import config
import time

print("[BOOT] Iniciando SPI y montaje de SD...")

try:
    spi = SPI(2, baudrate=1000000, sck=Pin(config.SPI_SCK), mosi=Pin(config.SPI_MOSI), miso=Pin(config.SPI_MISO))
    sd = sdcard.SDCard(spi, Pin(config.SD_CS))
    os.mount(sd, "/sd")
    print("[✔] SD montada correctamente. Archivos:", os.listdir("/sd"))
except Exception as e:
    print("[✘] Error al montar SD:", e)

time.sleep(1)

