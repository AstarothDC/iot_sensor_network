# config.py – configuración general del nodo

# Identificador único del nodo
NODE_ID = "nodo_01"

# Definir si este nodo es el nodo padre
IS_PARENT = False  # Cambiar a True solo en el nodo padre

# Pines I2C para sensores BME280 y RTC DS3231
I2C_SCL = 22
I2C_SDA = 21

# Pines UART para sensores RS485 (HD-38 y CWT)
UART_TX = 17
UART_RX = 16

# Pines para LoRa SX127x
LORA_CS = 15
LORA_RST = 14
LORA_IRQ = 4
LORA_FREQ = 915E6  # Puede ser 433E6, 868E6 o 915E6 según región

# Intervalo entre mediciones en segundos (ej. 1800s = 30 min)
READ_INTERVAL = 1800
