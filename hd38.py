# hd38.py – Lectura del sensor HD-38 (RS485/Modbus)

def read_hd38(uart):
    try:
        # Aquí iría una implementación real del protocolo Modbus
        # Por ahora, simulamos valores como ejemplo
        return {
            "soil_temp": 24.5,
            "soil_hum": 57.2
        }
    except Exception as e:
        print("Error leyendo HD-38:", e)
        return {"soil_temp": None, "soil_hum": None}
