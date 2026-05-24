'''
wennn file x groß ist und upload speed x dazu passt lade diese dateien. 
api key finder. first go to gitignore or look just for secret folder
'''
from pathlib import Path
import os
import paramiko
import stat


HOME = Path.home()
CURRENT = Path.cwd()
SCHREIBTISCH = HOME / "Schreibtisch" 
# Schreibtisch = German name for Desktop on macOS

def get_importent_files_by_extansion():

    for file in SCHREIBTISCH.rglob("*.py"):
        return file
    
file = Path("path_test.txt")

file_size = file.stat().st_size # size in bytes 

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

#-----------------------



mode = file.stat().st_mode
print(oct(mode))
print(stat.filemode(mode))


#------------------biggest files

big_data_files = []

def get_biggest():

    for file in HOME.rglob("*"):
        if file.is_file():
            try:
                size = file.stat().st_size
                big_data_files.append((size, file))
            except PermissionError:
                pass

#get_biggest()

big_data_files.sort(reverse=True) #biggest_first

for size, path in big_data_files[:20]:
    print(f"{size / 1024 / 1024:.2f} MB -> {path}")

#---------------------------

last_chnaged_files = []

def last_changed():
    
    for file in HOME.rglob("*"):
        if file.is_file:
            try:
                mtime = file.stat().st_mtime
                last_chnaged_files.append((mtime, file))
            except PermissionError:
                pass

last_changed()

last_chnaged_files.sort(reverse=True)

for mtime, path in last_chnaged_files[:20]:
    readable = last_chnaged_files.ctime(mtime)
    print(readable, "->", path)