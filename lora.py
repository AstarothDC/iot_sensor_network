def send_lora(data):
    try:
        print("[LoRa] Transmitiendo datos:", data)
        # Aquí debes integrar la librería específica de tu módulo SX127x
        # como pyLoRa, lopy-lora o adaptación propia
    except Exception as e:
        print("Error enviando por LoRa:", e)