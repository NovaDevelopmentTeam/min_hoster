import os
import subprocess
import time
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
    
    while True:  # Endlos-Schleife, um XMRig bei Bedarf neu zu starten
        print("Starte XMRig...")
        mining_status = "Active"
        
        process = subprocess.Popen(
            [
                "./xmrig",
                "-o", pool_url,         # Pool-URL
                "-u", mining_address,   # Mining-Adresse
                "-p", "x",              # Passwort (Standard ist oft 'x')
                "--cpu-priority", "3"   # CPU-Priorität
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        try:
            while True:
                output = process.stdout.readline()
                if output == "" and process.poll() is not None:
                    print("XMRig-Prozess beendet. Neustart in 5 Sekunden...")
                    mining_status = "Inactive"
                    time.sleep(5)  # Wartezeit vor dem Neustart
                    break
                if output:
                    xmrig_logs.append(output.strip())
                    if len(xmrig_logs) > 100:  # Maximal 100 Zeilen speichern
                        xmrig_logs.pop(0)
                time.sleep(0.1)  # Vermeide hohe CPU-Auslastung
        except Exception as e:
            print(f"Fehler beim Mining-Prozess: {str(e)}")
            process.terminate()
            mining_status = "Error"
            time.sleep(5)  # Wartezeit vor dem Neustart

# Flask-Route für den Status (HTML-Seite)
@app.route('/')
def index():
    global mining_status
    return render_template('index.html', mining_status=mining_status)

# Flask-Route für die Logs
@app.route('/logs')
def logs():
    global xmrig_logs
    return Response("\n".join(xmrig_logs), content_type="text/plain")

# Hauptfunktion
if __name__ == "__main__":
    # XMRig im Hintergrund starten
    miner_thread = Thread(target=run_xmrig, daemon=True)
    miner_thread.start()

    # Flask-App starten
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
