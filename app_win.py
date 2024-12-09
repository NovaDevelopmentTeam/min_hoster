import os
import subprocess
import time
from threading import Thread

# Globale Variablen
xmrig_logs = []  # Log-Speicher
mining_status = "Inactive"  # Initialer Status des Minings

# Deine Monero-Mining-Adresse (ersetzen durch deine echte Wallet-Adresse)
mining_address = "47SoHaddieiTiuTvczsrbvLdMMLYbk3wKjBbtag8xqErLsPwHABwCtHJiawhC7sS97WJd52KrL1cxTENHS4foTu98rHm1Gs"

# Pool-URL und Port
pool_url = "mine.xmrpool.net:3333"

# Funktion, um XMRig auszuführen
def run_xmrig():
    """
    Startet XMRig in einer Endlosschleife und überwacht den Prozess.
    """
    global xmrig_logs, mining_status

    # Pfad zur XMRig-Binärdatei (anpassen, falls nötig)
    xmrig_path = os.path.abspath("xmrig.exe")  # .exe für Windows

    if not os.path.exists(xmrig_path):
        print(f"Fehler: XMRig wurde nicht gefunden unter {xmrig_path}.")
        return

    while True:
        print("Starte XMRig...")
        mining_status = "Active"

        try:
            # Starte den XMRig-Prozess
            process = subprocess.Popen(
                [
                    xmrig_path,
                    "-o", pool_url,        # Pool-URL
                    "-u", mining_address,  # Mining-Adresse
                    "-p", "x",             # Passwort (oft Standard: 'x')
                    "--cpu-priority", "3"  # CPU-Priorität (3 = niedrig)
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )

            while True:
                # Lese die Prozessausgabe
                output = process.stdout.readline()
                if output == "" and process.poll() is not None:
                    print("XMRig-Prozess beendet. Neustart in 5 Sekunden...")
                    mining_status = "Inactive"
                    time.sleep(5)  # Wartezeit vor Neustart
                    break
                if output:
                    xmrig_logs.append(output.strip())
                    if len(xmrig_logs) > 100:  # Maximal 100 Zeilen speichern
                        xmrig_logs.pop(0)
                    print(output.strip())  # Ausgabe anzeigen
                time.sleep(0.1)  # Vermeidung von hoher CPU-Auslastung
        except Exception as e:
            print(f"Fehler beim Mining-Prozess: {str(e)}")
            mining_status = "Error"
            time.sleep(5)  # Wartezeit vor Neustart

# Hauptfunktion
if __name__ == "__main__":
    # Hinweis für den Benutzer
    print("Starte XMRig Miner... Drücke Strg+C zum Beenden.")
    
    # XMRig in einem separaten Thread starten
    miner_thread = Thread(target=run_xmrig, daemon=True)
    miner_thread.start()

    # Halte das Hauptprogramm am Laufen
    try:
        while True:
            print(f"Mining-Status: {mining_status}")
            time.sleep(10)  # Aktualisiere den Status alle 10 Sekunden
    except KeyboardInterrupt:
        print("\nProgramm beendet. Miner wird gestoppt.")
