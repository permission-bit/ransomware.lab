from pathlib import Path
import os


PATHS = [
    Path.home() / "Library/LaunchAgents",
    Path("/Library/LaunchAgents"),
    Path("/Library/LaunchDaemons"),
]


def find_writable_files() -> list[Path]:
    writable = []

    for base in PATHS:

        if not base.exists():
            continue

        for file in base.rglob("*"):

            if not file.is_file():
                continue

            if os.access(file, os.W_OK):
                writable.append(file)

    return writable


for item in find_writable_files():
    print(item)