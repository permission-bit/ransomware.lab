# file: tools/security_inventory.py

from pathlib import Path
import subprocess

APP_DIRS = [
    Path("/Applications"),
    Path("/System/Applications"),
    Path.home() / "Applications",
]

KEYWORDS = [
    # macOS / Apple
    "xprotect", "gatekeeper", "mrt", "filevault",

    # AV / EDR bekannte Namen
    "malwarebytes", "bitdefender", "avast", "avg", "norton",
    "sophos", "eset", "kaspersky", "mcafee", "trend micro",
    "sentinelone", "crowdstrike", "falcon", "defender",
    "microsoft defender", "carbon black", "vmware carbon black",
    "cylance", "blackberry", "palo alto", "cortex",
    "jamf", "objective-see", "lulu", "little snitch",
    "intego", "clamxav", "clamav", "f-secure", "withsecure",
    "fireeye", "trellix", "elastic", "osquery", "wazuh",
    "splunk", "rapid7", "qualys", "tenable",
]


def run(cmd: list[str]) -> str:
    try:
        return subprocess.check_output(cmd, text=True, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        return ""


def find_installed_apps() -> list[str]:
    found = []

    for app_dir in APP_DIRS:
        if not app_dir.exists():
            continue

        for app in app_dir.glob("*.app"):
            name = app.name.lower()
            if any(keyword in name for keyword in KEYWORDS):
                found.append(str(app))

    return sorted(set(found))


def find_running_processes() -> list[str]:
    output = run(["ps", "axo", "pid,comm"])
    found = []

    for line in output.splitlines():
        lower = line.lower()
        if any(keyword in lower for keyword in KEYWORDS):
            found.append(line.strip())

    return sorted(set(found))


def find_launch_services() -> list[str]:
    dirs = [
        Path("/Library/LaunchAgents"),
        Path("/Library/LaunchDaemons"),
        Path.home() / "Library/LaunchAgents",
    ]

    found = []

    for folder in dirs:
        if not folder.exists():
            continue

        for item in folder.glob("*.plist"):
            name = item.name.lower()
            if any(keyword in name for keyword in KEYWORDS):
                found.append(str(item))

    return sorted(set(found))


def print_section(title: str, items: list[str]) -> None:
    print(f"\n=== {title} ===")
    if not items:
        print("Nichts gefunden.")
        return

    for item in items:
        print(f"- {item}")


def main() -> None:
    print_section("Installierte Security-Apps", find_installed_apps())
    print_section("Laufende Security-Prozesse", find_running_processes())
    print_section("LaunchAgents / LaunchDaemons", find_launch_services())


if __name__ == "__main__":
    main()