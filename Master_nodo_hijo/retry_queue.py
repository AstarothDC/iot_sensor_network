# retry_queue.py – Reintentos de envío HTTP para nodo hijo

import ujson
import os

QUEUE_DIR = "/sd/pendientes"

# 🗂️ Crear carpeta si no existe
def init_queue():
    try:
        if "pendientes" not in os.listdir("/sd"):
            os.mkdir(QUEUE_DIR)
    except Exception as e:
        print("[⚠️] No se pudo crear carpeta de reintentos:", e)

# ➕ Agregar archivo JSON si el envío falla
def enqueue(data, timestamp):
    try:
        fname = f"{QUEUE_DIR}/fail_{timestamp.replace(':', '-')}.json"
        with open(fname, "w") as f:
            ujson.dump(data, f)
        print(f"[⬇] Guardado para reintento: {fname}")
    except Exception as e:
        print("[❌] Error guardando reintento:", e)

# 🔁 Procesar archivos pendientes
def process_queue(send_func):
    try:
        files = os.listdir(QUEUE_DIR)
        for fname in files:
            if fname.endswith(".json"):
                path = f"{QUEUE_DIR}/{fname}"
                with open(path) as f:
                    data = ujson.load(f)
                try:
                    if send_func(data):
                        os.remove(path)
                        print(f"[✔️] Reenviado y eliminado: {fname}")
                    else:
                        print(f"[⏳] Falló reenvío (se mantiene): {fname}")
                except Exception as e:
                    print(f"[!] Error reenviando {fname}:", e)
    except Exception as e:
        print("[❌] Error procesando reintentos:", e)
