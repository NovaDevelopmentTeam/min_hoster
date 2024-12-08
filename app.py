import os
import subprocess

# Setze Ausführungsrechte für die ausführbare Datei
os.chmod('./xmrig', 0o755)

# Deine Monero-Mining-Adresse (ersetzen durch deine echte Wallet-Adresse)
mining_address = "your-mining-address"

# Pool-URL und Port
pool_url = "mine.xmrpool.net:3333"

# Führe XMRig aus
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

# Ausgabe prüfen
print(result.stdout)
print(result.stderr)
