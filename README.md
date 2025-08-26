# Keylogger Académico con Dashboard

Proyecto de prueba para fines educativos y universitarios.

## Estructura

- `keylogger.py` → Captura teclas y las envía al servidor.
- `server.py` → Servidor Flask con dashboard en tiempo real.
- `captura_remota.txt` → Se genera automáticamente con teclas capturadas.
- `acciones.txt` → Historial de acciones (inicio, borrado, cierre).
- `log_local.txt` → Backup si no se puede enviar al servidor.
- `requirements.txt` → Dependencias.

## Instalación

1. Clonar el repositorio:
```bash
git clone <URL-del-repo>
cd Keylogger_flask
