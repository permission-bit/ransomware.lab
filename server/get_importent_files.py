from pathlib import Path

HOME = Path.home()

def get_importent_files_by_extansion():

    for file in Path(".").rglob("*.py"):
        return file

    
