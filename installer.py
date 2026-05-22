import shutil
import subprocess

TOOLS = [
    "nmap",
    "masscan",
    "git",
    "wget",
    "curl",
    "pyinstaller",
    "pip"
]


def detect_package_manager():

    managers = [
        "brew",
        "apt",
        "dnf",
        "pacman",
        "yum",
        "winget",
        "choco"
    ]

    for manager in managers:
        if shutil.which(manager):
            return manager

    return None


def build_command(manager: str, tool: str):

    commands = {
        "brew": ["brew", "install", tool],
        "apt": ["sudo", "apt", "install", "-y", tool],
        "dnf": ["sudo", "dnf", "install", "-y", tool],
        "pacman": ["sudo", "pacman", "-S", "--noconfirm", tool],
        "yum": ["sudo", "yum", "install", "-y", tool],
        "winget": ["winget", "install", tool],
        "choco": ["choco", "install", tool, "-y"],
    }

    return commands.get(manager)


def install_tools():

    manager = detect_package_manager()

    if not manager:
        print("[ERROR] No package manager found")
        return

    print(f"[INFO] Using package manager: {manager}")

    for tool in TOOLS:

        print(f"\n[CHECK] {tool}")

        # Prüfen ob Tool existiert
        if shutil.which(tool):

            tool_path = shutil.which(tool)

            print(f"[OK] {tool} already installed")
            print(f"[PATH] {tool_path}")

            continue

        print(f"[INSTALL] Installing {tool}...")

        cmd = build_command(manager, tool)

        if not cmd:
            print(f"[ERROR] Unsupported package manager")
            continue

        try:

            subprocess.run(cmd, check=True)

            print(f"[SUCCESS] {tool} installed")

        except subprocess.CalledProcessError:

            print(f"[FAILED] Could not install {tool}")


if __name__ == "__main__":
    install_tools()