import os
import subprocess
from flask import Flask, render_template, Response
from threading import Thread

# Flask-App erstellen
app = Flask(__name__)

# Globale Variablen
xmrig_logs = []
mining_status = "Inactive"  # Status des Minings (default: Inaktiv)

# Setze Ausführungsrechte für die ausführbare Datei
os.chmod('./xmrig', 0o755)

# Deine Monero-Mining-Adresse (ersetzen durch deine echte Wallet-Adresse)
mining_address = "47SoHaddieiTiuTvczsrbvLdMMLYbk3wKjBbtag8xqErLsPwHABwCtHJiawhC7sS97WJd52KrL1cxTENHS4foTu98rHm1Gs"

# Pool-URL und Port
pool_url = "mine.xmrpool.net:3333"

# Funktion, um XMRig auszuführen
def run_xmrig():
    global xmrig_logs, mining_status
    mining_status = "Active"  # Setze den Mining-Status auf "aktiv"
    
    print("Starte XMRig...")

    process = subprocess.Popen(
        [
            "./xmrig",
            "-o", pool_url,         # Pool-URL
            "-u", mining_address,   # Mining-Adresse
            "-p", "x",              # Passwort (Standard ist oft "x")
            "--cpu-priority", "3"   # CPU-Priorität
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    # Log-Ausgabe sammeln
    for line in process.stdout:
        print(f"Logzeile: {line.strip()}")
        xmrig_logs.append(line)
        if len(xmrig_logs) > 100:  # Maximal 100 Zeilen speichern
            xmrig_logs.pop(0)

# Flask-Route für den Status (HTML-Seite)
@app.route('/')
def index():
    global mining_status
    return render_template('index.html', mining_status=mining_status)

# Flask-Route für die Logs
@app.route('/logs')
def logs():
    global xmrig_logs
    try:
        print(f"Logs: {len(xmrig_logs)} Einträge")
        return Response("\n".join(xmrig_logs), content_type="text/plain")
    except Exception as e:
        print(f"Fehler beim Laden der Logs: {str(e)}")
        return f"Fehler beim Laden der Logs: {str(e)}", 500

# Hauptfunktion
if __name__ == "__main__":
    # XMRig im Hintergrund starten
    print("Starte Mining...")
    miner_thread = Thread(target=run_xmrig, daemon=True)
    miner_thread.start()

    # Flask-App starten
    print("Starte Flask-App auf Port 10000...")
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
