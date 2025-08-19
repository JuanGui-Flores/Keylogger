from pynput import keyboard

contador = 0

def on_press(key):
    global contador
    contador += 1
    print(f"Teclas presionadas: {contador}")  # el usuario lo ve en consola

def on_release(key):
    if key == keyboard.Key.esc:
        return False

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
