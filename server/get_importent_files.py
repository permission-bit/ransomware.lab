from pathlib import Path
import os
import paramiko

HOME = Path.home()
CURRENT = Path.cwd()
SCHREIBTISCH = HOME / "Schreibtisch"

def get_importent_files_by_extansion():

    for file in SCHREIBTISCH.rglob("*.py"):
        return file
    
p = Path("path_test.txt")

file_size = p.stat().st_size # size in bytes 

def make_file_size_beauty(file_size: int):

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

