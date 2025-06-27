import time
from machine import Pin, ADC, I2C, deepsleep
from config import *
from wifi_client import connect_wifi, disconnect_wifi
from http_client import get_remote_time, send_data
from rtc_ds1307 import RTC_DS1307, setup_rtc
from bme280 import read_bme
from hd38 import HD38
from cwt_soil import CWT_Soil
from sd_utils import save_json, copy_json

# 🔌 Inicializar GPIO
led = Pin(LED_PIN, Pin.OUT)
relay = Pin(RELAY_PIN, Pin.OUT)
led.value(1)
relay.value(1)

print(f"🔋 Nodo hijo {NODE_ID} iniciando...")

# 🕒 Inicializar RTC
i2c = I2C(1, scl=Pin(I2C_SCL), sda=Pin(I2C_SDA))
rtc = RTC_DS1307(i2c)

# 🌐 Conexión Wi-Fi
wifi_ok = connect_wifi(WIFI_SSID, WIFI_PASS, WIFI_TIMEOUT_MS)

# ⏱️ Sincronizar hora
if wifi_ok:
    hora_remota = get_remote_time()
    if hora_remota:
        rtc.set_time_from_string(hora_remota)
        print("✅ RTC sincronizado:", hora_remota)
    else:
        print("⚠️ No se pudo sincronizar la hora")
else:
    print("⚠️ Sin Wi-Fi, solo se usará SD")

# 🕒 Timestamp actual
timestamp = rtc.get_timestamp()
print("🕒 Timestamp:", timestamp)

# 🌡️ Lectura sensores
ambient = read_bme(i2c)
print("🌤️ BME280:", ambient)

hd_sensor = HD38(HD38_PIN)
soil_hum = {"soil_hum": hd_sensor.read_percent()}
print("🌱 HD38:", soil_hum)

cwt_sensor = CWT_Soil(CWT_TX, CWT_RX, CWT_DE_RE)
soil_data = cwt_sensor.read_values()
print("🧪 CWT:", soil_data)

# 🧩 Unir todo
data = {
    "id": NODE_ID,
    "timestamp": timestamp,
    "ambient": ambient,
    "soil": {**soil_hum, **soil_data}
}

# 💾 Guardar en SD
save_json(data, PATH_FILE)
copy_json(data, PATH_COPY)
save_json(data, PATH_TOTAL)

# 📡 Enviar si hay red
if wifi_ok:
    try:
        sent = send_data(data)
        if sent:
            print("✅ Datos enviados con éxito")
        else:
            print("⚠️ Fallo en envío HTTP")
    except Exception as e:
        print("❌ Error al enviar:", e)
else:
    print("📂 Datos guardados en SD por falta de conexión")

# 💤 Prepararse para dormir
disconnect_wifi()
print(f"😴 Deep sleep por {SAMPLING_TIME_MS // 60000} min...")
time.sleep(1)
deepsleep(SAMPLING_TIME_MS)
