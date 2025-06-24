# main.py – lógica principal del nodo IoT (padre o hijo)

from machine import I2C, UART
import time
import config
import bme280, hd38, cwt_soil, rtc_ds3231, sdcard, lora, lte, utils

# Inicializar interfaces
i2c = I2C(0, scl=config.I2C_SCL, sda=config.I2C_SDA)
uart = UART(1, tx=config.UART_TX, rx=config.UART_RX, baudrate=9600)


def run_cycle():
    timestamp = rtc_ds3231.get_timestamp(i2c)
    ambient = bme280.read_bme(i2c)
    soil_hd = hd38.read_hd38(uart)
    soil_cwt = cwt_soil.read_cwt(uart)

    data = {
        "id": config.NODE_ID,
        "timestamp": timestamp,
        "ambient": ambient,
        "soil": {**soil_hd, **soil_cwt}
    }

    # Guardar en microSD
    sdcard.save_data(data, timestamp)

    # Transmitir según rol del nodo
    if config.IS_PARENT:
        try:
            lte.send_to_server(data)
        except Exception as e:
            print("Error LTE:", e)
    else:
        try:
            lora.send_lora(data)
        except Exception as e:
            print("Error LoRa:", e)


def resend_pending():
    if config.IS_PARENT:
        files = utils.check_reconnect()
        for fname in files:
            with open("/sd/" + fname) as f:
                for line in f:
                    try:
                        lte.send_to_server(line)
                    except:
                        continue


while True:
    run_cycle()
    resend_pending()
    time.sleep(config.READ_INTERVAL)