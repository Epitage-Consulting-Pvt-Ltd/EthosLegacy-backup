import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QPushButton, QMessageBox

# Function to set the Wi-Fi details
def set_wifi_details(ssid, password):
    try:
        subprocess.check_output(['sudo', 'nmcli', 'dev', 'wifi', 'disconnect'])
        subprocess.check_output(['sudo', 'nmcli', 'device', 'wifi', 'connect', ssid, 'password', password])
        return "Success: Wi-Fi details updated."
    except subprocess.CalledProcessError:
        return "Error: Failed to set Wi-Fi details."

class NetworkSettingsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set window properties
        self.setWindowTitle('Network Settings')
        self.setGeometry(100, 100, 400, 200)

        # Create labels and input fields for Wi-Fi parameters
        ssid_label = QLabel('SSID:')
        self.ssid_textbox = QLineEdit()
        password_label = QLabel('Password:')
        self.password_textbox = QLineEdit()
        self.password_textbox.setEchoMode(QLineEdit.Password)

        # Create a button to update Wi-Fi details
        set_button = QPushButton('Set Details')

        # Create a layout and add widgets to it
        layout = QVBoxLayout()
        layout.addWidget(ssid_label)
        layout.addWidget(self.ssid_textbox)
        layout.addWidget(password_label)
        layout.addWidget(self.password_textbox)
        layout.addWidget(set_button)

        # Set the layout for the main window
        self.setLayout(layout)

        # Connect button click event to the set_wifi_details function
        set_button.clicked.connect(self.set_wifi_details)

    def set_wifi_details(self):
        ssid = self.ssid_textbox.text()
        password = self.password_textbox.text()

        result = set_wifi_details(ssid, password)
        self.show_message(result)

    def show_message(self, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Wi-Fi Settings")
        msg_box.setText(message)
        msg_box.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = NetworkSettingsWindow()
    window.show()
    sys.exit(app.exec_())
