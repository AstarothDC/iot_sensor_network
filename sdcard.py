# sdcard.py – Funciones para guardar datos en microSD en formato JSON

import ujson

def save_data(data, timestamp):
    try:
        date_str = timestamp[:10]  # YYYY-MM-DD
        filename = "/sd/" + date_str + ".json"
        with open(filename, "a") as f:
            ujson.dump(data, f)
            f.write("\n")
        print("✔ Datos guardados en SD")
    except Exception as e:
        print("⚠ Error al guardar en SD:", e)
