from pathlib import Path
import os
import stat
from datetime import datetime
import time
import speedtest
from server.get_importent_files import get_importent_files_by_extansion, make_file_size_beauty, get_biggest, last_changed, get_importent_developer_files, get_folder_size

IMPORTANT_FILES = get_importent_files_by_extansion
PRETTY_FILES = make_file_size_beauty
BIGGEST_LOSER = get_biggest
LAST_CHANGED = last_changed
DEV_FILES = get_importent_developer_files
FOLDER_SIZE = get_folder_size

HOME = Path.home()
CURRENT = Path.cwd()
SCHREIBTISCH = HOME / "Desktop" 


IMPORTANT_NAMES = {
    "pyproject.toml",
    "package.json",
    ".env",
    "requirements.txt",
    "docker-compose.yml",
    "Cargo.toml",
}

IMPORTANT_EXTENSIONS = {
    ".py",
    ".rs",
    ".js",
    ".ts",
    ".json",
    ".toml",
    ".yaml",
    ".yml",
}

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


def messure_upload():

    try:
        speed = measure_upload_mbit()
        #print(f"Upload: {speed:.2f} Mbit/s")

        transfer_amount = get_transfer_amount(speed)

        # with open("transfer_amount.json", "w") as f:
        #     json.dump({"transfer_bytes": transfer_amount}, f, indent=2)

    except Exception as e:
        #print("Speedtest failed:", e)
        return transfer_amount




def get_importent_files_by_extansion():

    for file in SCHREIBTISCH.rglob("*.py"):
        return file
    
file = Path("path_test.txt")

file_size = file.stat().st_size # size in bytes


# print("[*] Load importent extansion files...")
# print(get_importent_files_by_extansion())



def make_file_size_beauty():

    if file_size < 1024:
        return f"{file_size} B"

    elif file_size < 1024 ** 2:
        return f"{file_size / 1024:.2f} KB"

    elif file_size < 1024 ** 3:
        return f"{file_size / (1024 ** 2):.2f} MB"

    else:
        return f"{file_size / (1024 ** 3):.2f} GB"

'''
unit 	Bytes

1 KB	1 024 Bytes
1 MB	1 048 576 Bytes
1 GB	1 073 741 824 Bytes
1 TB	1 099 511 627 776 Bytes

MB → 1024 * 1024
GB → 1024 * 1024 * 1024
'''
# print(file_size)

# print(make_file_size_beauty())
# print(10*"-")

#-----------------------



# mode = file.stat().st_mode
# print(oct(mode))
# print(stat.filemode(mode))
# print(10*"-")


#------------------biggest files

big_data_files = []

def get_biggest():

    for file in SCHREIBTISCH.rglob("*"):
        if file.is_file():
            try:
                size = file.stat().st_size
                big_data_files.append((size, file))
            except PermissionError:
                pass



    big_data_files.sort(reverse=True) #biggest_first

    result = []

    for size, path in big_data_files[:20]:

        result.append(
            f"{size / 1024 / 1024:.2f} MB -> {path}"
        ) 

    return result

# print("[*] Load get_biggest()...")

# print(get_biggest())
# print(10*"-")

#---------------------------

last_changed_files = []


def last_changed():

    for file in SCHREIBTISCH.rglob("*"):

        if file.is_file():

            try:
                mtime = file.stat().st_mtime
                last_changed_files.append((mtime, file))

            except PermissionError:
                pass

    # newest first
    last_changed_files.sort(reverse=True)

    result = []

    for mtime, path in last_changed_files[:20]:

        readable = time.ctime(mtime)

        result.append(
            f"{readable} -> {path}"
        )

    return result

# print("[*] Load last changed files...")
# print("\n".join(last_changed()))
# print(10*"-")


#------------get dev files

def get_importent_developer_files():
    for file in SCHREIBTISCH.rglob("*"):
        if file.name in IMPORTANT_NAMES:
            return file
        

# print("[*] Load developer files...")
# print(get_importent_developer_files())
# print(10*"-")

#-----------------biggest folder

folder_sizes = {}  # {folder: size}


def get_folder_size():

    for file in SCHREIBTISCH.rglob("*"):

        if file.is_file():

            try:
                size = file.stat().st_size
                parent = file.parent

                folder_sizes[parent] = (
                    folder_sizes.get(parent, 0) + size
                )

            except PermissionError:
                pass

    sorted_dirs = sorted(
        folder_sizes.items(),
        key=lambda x: x[1],
        reverse=True
    )

    result = []

    for folder, size in sorted_dirs[:20]:

        result.append(
            f"{size / 1024 / 1024:.2f} MB -> {folder}"
        )

    return result

# print("[*] Load biggest folder...")
# print("\n".join(get_folder_size()))
# print(10*"-")

#---------priority

def calculate_priority(file: Path) -> int:
    score = 0

    if file.name in IMPORTANT_NAMES:
        score += 1000

    if file.suffix in IMPORTANT_EXTENSIONS:
        score +=200

    try:
        stat = file.stat()

        size = file.stat().st_size
        modified = stat.st_mtime

        # smaller files first
        if size < 50_000:
            score += 100

        elif size < 500_000:
            score +50

        age_hours = (time.time() - modified) / 3600

        if age_hours < 24:
            score += 300

        if age_hours < 72:
            score += 150

        elif age_hours < 168:
            score += 50

    except Exception:
        pass

    return score