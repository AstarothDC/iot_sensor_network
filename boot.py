# boot.py – configuración de arranque y montaje de SD

from machine import Pin, SPI
import os
import sdcard
import time

# Configuración del SPI para la SD
spi = SPI(2, baudrate=1000000, sck=Pin(18), mosi=Pin(23), miso=Pin(19))
sd = sdcard.SDCard(spi, Pin(5))  # CS en GPIO 5

# Montar el sistema de archivos
try:
    os.mount(sd, "/sd")
    print("✔ SD montada correctamente")
    print("Archivos existentes:", os.listdir("/sd"))
except Exception as e:
    print("⚠ Error al montar SD:", e)

# Espera corta por seguridad en arranque
time.sleep(1)
