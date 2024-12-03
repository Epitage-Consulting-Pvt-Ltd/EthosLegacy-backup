# TODO: Code cleanup required.
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QWidget, QDialog, QLabel
from PyQt5.QtCore import Qt
from time import sleep


class PopupDialog(QDialog):
    def __init__(self, scan_result="Denied", employee_details=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Popup Dialog")
        self.setWindowFlag(Qt.FramelessWindowHint)

        layout = QVBoxLayout(self)
        if employee_details:
            label_text = employee_details
        else:
            label_text = scan_result

        label = QLabel(label_text, self)
        label.setStyleSheet("font: bold 16px;")

        # Set text color based on scan_result
        if scan_result == "Denied":
            label.setStyleSheet("color: red;")
        elif scan_result == "Verified":
            label.setStyleSheet("color: green;")

        label.setAlignment(Qt.AlignCenter)

        # self.setStyleSheet("background-color: orange; border: 2px black; border-radius: 5px;")
        layout.addWidget(label)

        self.setFixedSize(300, 100)  # Fixing size

    def auto_close(self):
        self.accept()

class AcceptDialog(QDialog):
    def __init__(self, scan_result="Verified", employee_details=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Dialog")
        self.setWindowFlag(Qt.FramelessWindowHint)

        layout = QVBoxLayout(self)
        if employee_details:
            label_text = f"Verified!\nEmployee Details:\n{employee_details}"
        else:
            label_text = "Verified!"

        label = QLabel(label_text, self)
        label.setStyleSheet("font: bold 16px;")

        # Set text color based on scan_result
        if scan_result == "Denied":
            label.setStyleSheet("color: red;")
        elif scan_result == "Verified":
            label.setStyleSheet("color: green;")

        label.setAlignment(Qt.AlignCenter)

        # self.setStyleSheet("background-color: orange; border: 2px black; border-radius: 5px;")
        layout.addWidget(label)

        self.setFixedSize(300, 100)  # Fixing size

    def auto_close(self):
        self.accept()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.button = QPushButton('Show Popup', self)
        self.button.clicked.connect(self.show_popup)

        layout = QVBoxLayout(self)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def show_popup(self):
        scan_result = "Denied"  # Simulated scan result, replace with actual logic to determine the scan result
        popup = PopupDialog(scan_result, self)
        popup.setGeometry(100, 100, 200, 100)
        popup.show()

        sleep(1)
        popup.auto_close()

    def accepted(self, employee_details=None):
        scan_result = "Verified"  # Simulated scan result, replace with actual logic to determine the scan result
        acc_popup = AcceptDialog(scan_result, employee_details, self)
        acc_popup.setGeometry(100, 100, 200, 100)
        acc_popup.show()
        sleep(1)
        acc_popup.auto_close()
