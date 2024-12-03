# TODO: Code not required, need to remove
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, QTimer

class PopupApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.FramelessWindowHint)  # Remove title bar and window controls
        self.setGeometry(100, 100, 200, 100)

        self.setup_ui()

        # Create a timer to close the popup after 5 seconds
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.close_popup)
        self.timer.start(5000)  # 5000 milliseconds = 5 seconds

    def setup_ui(self):
        layout = QVBoxLayout(self)

        label = QLabel("Registered Succesfully", self)
        label.setStyleSheet("font: bold 22px; color: white;")
        label.setAlignment(Qt.AlignCenter)

        self.setStyleSheet("background-color: green; border: 5px solid #808080; border-radius: 5px;")
        layout.addWidget(label)

    def close_popup(self):
        self.timer.stop()  # Stop the timer
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    popup_app = PopupApp()
    popup_app.show()
    sys.exit(app.exec_())
