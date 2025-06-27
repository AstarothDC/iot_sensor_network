# lte_queue.py – Sistema de cola para reintentos de envío LTE en caso de fallo

import ujson
import os

QUEUE_DIR = "/sd/pendientes"

# Asegura que el directorio exista
def init_queue():
    try:
        if "pendientes" not in os.listdir("/sd"):
            os.mkdir(QUEUE_DIR)
    except Exception as e:
        print("[ERROR] Creando carpeta de reintentos:", e)

# Guardar un paquete no enviado
def enqueue(data, timestamp):
    try:
        fname = f"{QUEUE_DIR}/fail_{timestamp.replace(':', '-')}.json"
        with open(fname, "w") as f:
            ujson.dump(data, f)
        print(f"[⬇] Guardado en cola de reintento: {fname}")
    except Exception as e:
        print("[ERROR] Al guardar en cola LTE:", e)

# Intentar reenviar todos los archivos pendientes
def process_queue(sender_func):
    try:
        for fname in os.listdir(QUEUE_DIR):
            if fname.endswith(".json"):
                path = f"{QUEUE_DIR}/{fname}"
                with open(path) as f:
                    data = ujson.load(f)
                try:
                    sender_func(data)
                    os.remove(path)
                    print(f"[✔] Reenviado y eliminado: {fname}")
                except Exception as e:
                    print(f"[!] Falló reenvío de {fname}:", e)
    except Exception as e:
        print("[ERROR] Procesando cola LTE:", e)
