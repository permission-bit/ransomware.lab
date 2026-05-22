import platform
import subprocess
import shutil

def get_arch():
    machine = platform.machine().lower()

    if machine == "arm64":
        return "apple silicon"
    elif machine in ("x86_64", "i386"):
        return "intel"
    return "unknown"

def get_macos_version(): 
    return platform.mac_ver()[0] # [0] = first element of a tuple 


def run(cmd, check=True):
    # Logs the command that is about to be executed for debugging purposes
    print(f"[RUN] {' '.join(cmd)}")
    
    # Executes the command using subprocess
    # cmd: list of command arguments (e.g. ["ls", "-la"])
    # check=True will raise an exception if the command fails
    return subprocess.run(cmd, check=check)


def exists(cmd):
    # Checks if a command exists in the system PATH
    # Returns True if the command is found, otherwise False
    return shutil.which(cmd) is not None