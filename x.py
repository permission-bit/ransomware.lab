from pathlib import Path
import platform


def get_all_paths() -> list[Path]:
    
    home = Path.home()
    system = platform.system()

    base_dirs: list[Path] = []

    if system == "Windows":
        base_dirs.extend([
            home / "Desktop",
            home / "Documents",
            home / "Downloads",
            home / "Pictures",
            home / "Videos",
            home / "Music",

            home / "AppData/Local",
            home / "AppData/Roaming",
            home / "AppData/LocalLow",

            Path("C:/ProgramData"),
            Path("C:/Temp"),
        ])

    elif system == "Darwin":
        base_dirs.extend([
            home / "Desktop",
            home / "Documents",
            home / "Downloads",
            home / "Pictures",
            home / "Movies",
            home / "Music",
            home / "Public",

            home / "Library",
            home / "Library/Application Support",
            home / "Library/Caches",
            home / "Library/Preferences",
            home / "Library/Logs",
            home / "Library/Containers",
            home / "Library/CloudStorage",
            home / "Library/Mobile Documents",
        ])

    else:
        base_dirs.extend([
            home / "Desktop",
            home / "Documents",
            home / "Downloads",
            home / "Pictures",
            home / "Videos",
            home / "Music",
            home / "Public",
            home / "Templates",

            home / ".config",
            home / ".cache",
            home / ".local/share",
            home / ".ssh",
            home / ".gnupg",
        ])

    all_paths: list[Path] = []

    for base in base_dirs:
        if not base.exists():
            continue

        try:
            # include base dir itself
            all_paths.append(base.resolve())

            # recursive
            for path in base.rglob("*"):
                try:
                    all_paths.append(path.resolve())
                except Exception:
                    pass

        except PermissionError:
            pass

    return all_paths


for path in get_all_paths():
    print(path)