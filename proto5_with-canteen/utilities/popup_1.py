# TODO: Code not required, need to remove
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QApplication
from PyQt5.QtCore import Qt


class AcceptDialog(QDialog):
    def __init__(self, message, parent=None):
        super().__init__(parent)
        self.setWindowTitle("RFID Card Scanner")
        self.setWindowFlag(Qt.FramelessWindowHint)

        layout = QVBoxLayout(self)

        label = QLabel(message, self)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet(
            "font: bold 16px; background-color: white; border: 2px solid orange;")

        layout.addWidget(label)

        self.setFixedSize(300, 100)  # Fixing size


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    dialog = AcceptDialog("Scanning RFID card...")
    dialog.exec_()
    sys.exit(app.exec_())
