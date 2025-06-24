# sx127x.py – Módulo para manejar el LoRa SX127x con MicroPython
# Requiere la librería sx127x adaptada para MicroPython (no oficial)

from machine import SPI, Pin
from sx127x import SX127x
import time
import ujson

class LoRaRadio:
    def __init__(self, spi, cs, reset, irq, frequency=915E6):
        self.lora = SX127x(spi=spi, cs=cs, reset=reset, irq=irq,
                           freq=frequency, bw=125E3, sf=7, cr=5)
        self.lora.set_coding_rate(5)
        self.lora.set_spreading_factor(7)
        self.lora.set_bandwidth(125000)
        self.lora.set_tx_power(17)

    def send(self, data):
        try:
            payload = ujson.dumps(data)
            self.lora.send(payload)
            print("✔ Datos enviados por LoRa")
        except Exception as e:
            print("⚠ Error enviando por LoRa:", e)

    def receive(self):
        try:
            packet = self.lora.recv()
            if packet:
                print("[LoRa] Paquete recibido:", packet)
                return ujson.loads(packet)
        except Exception as e:
            print("Error recibiendo por LoRa:", e)
        return None