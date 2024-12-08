import subprocess

# Run the binary and capture the output
result = subprocess.run(["./xmrig", "--some-arg"], capture_output=True, text=True)
print("Output:", result.stdout)
print("Errors:", result.stderr)
