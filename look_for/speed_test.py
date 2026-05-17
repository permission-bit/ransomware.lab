# upload_speed.py

import speedtest

s = speedtest.Speedtest()

s.get_best_server()

upload = s.upload()

print(f"{upload / 1_000_000:.2f} Mbit/s")