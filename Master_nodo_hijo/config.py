# config.py – Configuración del nodo hijo MicroPython

# Identificador y archivos
NODE_ID = "35"
PATH_FILE = "CSVnodoHijo_35.json"
PATH_COPY = "CopiaCSVnodoHijo_35.json"
PATH_TOTAL = "dataTotal_hijo_35.json"

# Wi-Fi del nodo padre
WIFI_SSID = "NodoPadre_AP"
WIFI_PASS = "12345678"

# Servidor (nodo padre)
SERVER_URL = "http://192.168.4.1"
PATH_DATA = "/data"
PATH_HORA = "/hora"

# Pines I2C para BME280 y RTC
I2C_SCL = 22
I2C_SDA = 21

# Pin ADC para HD-38
HD38_PIN = 26

# Pines para RS485 (sensor CWT)
CWT_TX = 17
CWT_RX = 16
CWT_DE_RE = 15

# Pines adicionales
BATTERY_ADC_PIN = 33
LED_PIN = 32
RELAY_PIN = 25

# Deep Sleep y tiempos
SAMPLING_TIME_MS = 3600000        # 1 hora = 3600000 ms
WIFI_TIMEOUT_MS = 180000          # Tiempo máximo para conexión Wi-Fi


