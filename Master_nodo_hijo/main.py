from machine import I2C, deepsleep, Pin
import time
import config
from wifi_client import connect_wifi, disconnect_wifi
from http_client import get_remote_time, send_data
from rtc_ds1307 import RTC_DS1307
from sd_utils import save_json, copy_json
from power_control import power_on_all, power_off_all
from hd38 import HD38
from cwt_soil import CWT_Soil
from bme280 import read_bme
from retry_queue import init_queue, enqueue, process_queue

print(f"\n🚀 Nodo hijo {config.NODE_ID} iniciando...")

# 🕒 RTC vía I2C
i2c = I2C(0, scl=Pin(config.I2C_SCL), sda=Pin(config.I2C_SDA))
rtc = RTC_DS1307(i2c)

# Inicializar sistema de reintentos
init_queue()

# 🌐 Conexión Wi-Fi al nodo padre
wifi_ok = connect_wifi(config.WIFI_SSID, config.WIFI_PASS, config.WIFI_TIMEOUT_MS)

# ⏱️ Sincronizar hora si hay red
if wifi_ok:
    remote_time = get_remote_time()
    if remote_time:
        rtc.set_time_from_string(remote_time)
        print("✅ RTC sincronizado:", remote_time)
    else:
        print("⚠️ No se pudo obtener hora del nodo padre")
else:
    print("⚠️ Nodo sin Wi-Fi, se usará hora RTC local")

# 🕒 Timestamp actual
timestamp = rtc.get_timestamp()
print("[⏰] Timestamp:", timestamp)

# ⚡ Encender sensores
power_on_all()
time.sleep(2)  # estabilización

# 📏 Lectura de sensores
hd_sensor = HD38(config.HD38_ADC_PIN)
hd = hd_sensor.read_percent()
print("[HD-38] Humedad del suelo:", hd)

cwt_sensor = CWT_Soil(tx_pin=config.UART_RS485_TX,
                      rx_pin=config.UART_RS485_RX,
                      de_re_pin=config.RS485_DE_RE)
cwt_data = cwt_sensor.read_values()
print("[CWT] Lectura:", cwt_data)

ambient = read_bme(i2c)
print("[BME280] Lectura:", ambient)

# 🧩 Unir todos los datos
soil = {"hd38": hd}
soil.update(cwt_data)

data = {
    "id": config.NODE_ID,
    "timestamp": timestamp,
    "ambient": ambient,
    "soil": soil
}

# 💾 Guardar en SD
save_json(data, config.PATH_FILE)
copy_json(data, config.PATH_COPY)
save_json(data, config.PATH_TOTAL)
print("💾 Datos almacenados localmente")

# 📡 Reintentos anteriores (si hay red)
if wifi_ok:
    print("🔁 Procesando reintentos previos...")
    process_queue(send_data)

# 📤 Enviar dato actual
if wifi_ok:
    try:
        if send_data(data):
            print("✅ Datos enviados al nodo padre")
        else:
            print("⚠️ Fallo en envío actual, se guardará para reintento")
            enqueue(data, timestamp)
    except Exception as e:
        print("❌ Error al enviar:", e)
        enqueue(data, timestamp)
else:
    print("📂 Sin Wi-Fi: dato guardado para reintento")
    enqueue(data, timestamp)

# 🔌 Apagar sensores y Wi-Fi
power_off_all()
disconnect_wifi()
time.sleep(1)

# 😴 Deep Sleep
print(f"😴 Deep sleep por {config.SAMPLING_TIME_MS // 60000} min...\n")
deepsleep(config.SAMPLING_TIME_MS)

