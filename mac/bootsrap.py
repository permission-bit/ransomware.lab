import platform

def get_arch():
    machine = platform.machine().lower()

    if machine == "arm64":
        return "apple silicon"
    elif machine in ("x86_64", "i386"):
        return "intel"
    return "unknown"

