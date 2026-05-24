'''
wennn file x groß ist und upload speed x dazu passt lade diese dateien. 
api key finder. first go to gitignore or look just for secret folder
'''
from pathlib import Path
import os
import stat
from datetime import datetime
import time



HOME = Path.home()
CURRENT = Path.cwd()
SCHREIBTISCH = HOME / "Desktop" 
# Schreibtisch = German name for Desktop on macOS

IMPORTANT = {
    "pyproject.toml",
    "package.json",
    ".env",
    "requirements.txt",
    "docker-compose.yml",
    "Cargo.toml",
}

def get_importent_files_by_extansion():

    for file in SCHREIBTISCH.rglob("*.py"):
        return file
    
file = Path("path_test.txt")

file_size = file.stat().st_size # size in bytes

print(get_importent_files_by_extansion())

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
print(file_size)

print(make_file_size_beauty())
print(10*"-")

#-----------------------



mode = file.stat().st_mode
print(oct(mode))
print(stat.filemode(mode))
print(10*"-")


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

print(get_biggest())
print(10*"-")

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


print("\n".join(last_changed()))
print(10*"-")


#------------get dev files

def get_importent_developer_files():
    for file in SCHREIBTISCH.rglob("*"):
        if file.name in IMPORTANT:
            return file
        
print(get_importent_developer_files())
print(10*"-")

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


print("\n".join(get_folder_size()))
print(10*"-")