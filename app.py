import os
import subprocess
from flask import Flask

# Flask-App erstellen, um einen Port für Render zu öffnen
app = Flask(__name__)

@app.route('/')
def status():
    return "XMRig is running on Render!"

# Setze Ausführungsrechte für die ausführbare Datei
os.chmod('./xmrig', 0o755)

# Deine Monero-Mining-Adresse (ersetzen durch deine echte Wallet-Adresse)
mining_address = "0x98722BBd5E467437b231c5B02bb021848D41492f"

# Pool-URL und Port
pool_url = "mine.xmrpool.net:3333"

# Funktion, um XMRig auszuführen
def run_xmrig():
    result = subprocess.run(
        [
            "./xmrig",
            "-o", pool_url,         # Pool-URL
            "-u", mining_address,   # Mining-Adresse
            "-p", "x",              # Passwort (Standard ist oft "x")
            "--cpu-priority", "3"   # CPU-Priorität
        ],
        capture_output=True,
        text=True
    )
    print(result.stdout)
    print(result.stderr)

# XMRig im Hintergrund starten
if __name__ == "__main__":
    # Startet XMRig in einem separaten Thread
    from threading import Thread
    miner_thread = Thread(target=run_xmrig, daemon=True)
    miner_thread.start()

    # Flask-App starten, um einen Port für Render bereitzustellen
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
