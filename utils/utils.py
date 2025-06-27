# utils.py – Funciones auxiliares para verificación y reintento

import os

def check_reconnect():
    try:
        files = os.listdir("/sd")
        return [f for f in files if f.endswith(".json")]
    except Exception as e:
        print("Error al listar archivos en SD:", e)
        return []
