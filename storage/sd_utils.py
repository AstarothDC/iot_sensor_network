import ujson
import os

def append_json(data, filename):
    path = "/sd/" + filename
    try:
        with open(path, "a") as f:
            ujson.dump(data, f)
            f.write("\n")
        print("✔ Datos guardados en:", path)
    except Exception as e:
        print("Error guardando en SD:", e)

def list_files():
    try:
        return os.listdir("/sd")
    except Exception as e:
        print("Error listando SD:", e)
        return []