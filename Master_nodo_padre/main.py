# main.py – Ciclo principal del nodo padre (lectura, almacenamiento, envío y servidor Wi-Fi)

from machine import I2C
import time
import config
from hd38 import HD38
from cwt_soil import CWT_Soil
from sim800l import SIM800L  # LTE desactivado temporalmente
from rtc_ds1307 import RTC_DS1307
from sd_utils import append_json
from bme280 import read_bme
import uasyncio as asyncio
from wifi_server import start_server
from lte_queue import init_queue, enqueue, process_queue

# Inicialización de sensores y periféricos
print("🚀 Iniciando nodo padre...")
i2c = I2C(0, scl=config.I2C_SCL, sda=config.I2C_SDA)
rtc = RTC_DS1307(i2c)
hd38 = HD38(config.HD38_ADC_PIN)
cwt = CWT_Soil(tx_pin=config.UART_RS485_TX, rx_pin=config.UART_RS485_RX, de_re_pin=config.RS485_DE_RE)
modem = SIM800L()  # LTE 
init_queue()

# Bucle de toma de datos
async def run_cycle():
    while True:
        timestamp = rtc.get_timestamp()
        print("\n[⏰] Timestamp:", timestamp)

        # 📏 Lectura de sensores
        hd = hd38.read_percent()
        print("[HD-38] Humedad del suelo (%):", hd)

        cwt_raw = cwt.read_values()
        print("[CWT] Datos recibidos:")
        for k, v in cwt_raw.items():
            print(f"   - {k}: {v}")

        ambient = read_bme(i2c)
        print("[BME280] Lectura ambiental:")
        for k, v in ambient.items():
            print(f"   - {k}: {v}")

        # 🧩 Ensamble de datos
        soil_data = {"hd38": hd}
        soil_data.update(cwt_raw)

        data = {
            "id": config.NODE_ID,
            "timestamp": timestamp,
            "ambient": ambient,
            "soil": soil_data
        }

        # 💾 Guardar en SD
        append_json(data, timestamp[:10] + ".json")
        print("[💾] Datos almacenados en SD")

        # 🔁 Reintentos de envío LTE
        print("[📡] Procesando cola de reintentos LTE...")
        process_queue(modem.send_json)

        # 🚀 Intentar enviar el dato actual
        try:
            modem.send_json(data)
            print("[✉️] Datos enviados correctamente vía LTE")
        except Exception as e:
            print("[!] Error en envío LTE:", e)
            enqueue(data, timestamp)

        await asyncio.sleep(config.READ_INTERVAL)

# Función principal asíncrona
async def main():
    await asyncio.gather(
        start_server(),
        run_cycle()
    )

# Ejecución compatible con MicroPython
loop = asyncio.get_event_loop()
loop.run_until_complete(main())

