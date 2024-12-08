import os
import subprocess

# Setze Ausführungsrechte
os.chmod('./xmrig', 0o755)

# Führe die Datei aus
result = subprocess.run(["./xmrig", "--some-arg"], capture_output=True, text=True)
print(result.stdout)
print(result.stderr)
