import psutil

def get_processes():
    processes = {}

    for proc in psutil.process_iter([
        "pid",             # Process ID
                            # Eindeutige Kennung des Prozesses im Betriebssystem.

        "ppid",            # Parent Process ID
                            # Prozess-ID des Elternprozesses.
                            # Hilfreich um Prozessketten zu analysieren.

        "name",            # Prozessname
                            # Kurzname des Prozesses.
                            # Beispiel: "python", "Safari", "nginx"

        "exe",             # Vollständiger Pfad zur ausführbaren Datei
                            # Beispiel:
                            # /usr/bin/python3
                            # /Applications/Safari.app/...

        "cmdline",         # Kommandozeilen-Argumente
                            # Zeigt wie der Prozess gestartet wurde.
                            # Beispiel:
                            # ["python3", "server.py", "--debug"]

        "status",          # Aktueller Status des Prozesses
                            # Beispiele:
                            # running
                            # sleeping
                            # stopped
                            # zombie

        "username",        # Benutzer des Prozesses
                            # Zeigt welcher User den Prozess gestartet hat.
                            # Beispiel:
                            # "root"
                            # "vincent"

        "create_time",     # Startzeit des Prozesses
                            # Unix-Timestamp wann der Prozess gestartet wurde.

        #"cpu_percent",     # CPU-Auslastung des Prozesses
                            # Prozentuale CPU-Nutzung.
                            # Kann über 100% gehen bei mehreren CPU-Kernen.

        #"memory_percent",  # RAM-Auslastung des Prozesses
                            # Prozentualer Anteil des Arbeitsspeichers.
    ]):
        try:
            info = proc.info
            processes[info["pid"]] = info
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    return processes


import psutil

def kill_process(pid: int):
    try:
        proc = psutil.Process(pid)
        proc.terminate()
        proc.wait(timeout=5)
        return True
    except Exception as e:
        print(e)
        return False




def find_by_name(name: str):
    result = []

    for proc in psutil.process_iter(["pid", "name"]):
        try:
            if name.lower() in proc.info["name"].lower():
                result.append(proc.info)
        except:
            pass

    return result