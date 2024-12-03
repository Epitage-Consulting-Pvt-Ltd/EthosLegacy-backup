import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QPushButton, QMessageBox
from qt_material import apply_stylesheet

# Function to set the network details
def set_network_details(ip_address, subnet_mask, gateway, dns_servers):
    try:
        subprocess.check_output(['sudo', 'ip', 'addr', 'flush', 'dev', 'eth0'])
        subprocess.check_output(['sudo', 'ip', 'addr', 'add', ip_address + '/' + subnet_mask, 'dev', 'eth0'])
        subprocess.check_output(['sudo', 'ip', 'route', 'del', 'default'])
        subprocess.check_output(['sudo', 'ip', 'route', 'add', 'default', 'via', gateway])
        with open('/etc/resolv.conf', 'w') as file:
            for dns_server in dns_servers:
                file.write('nameserver ' + dns_server + '\n')
        return "Success: Network details updated."
    except subprocess.CalledProcessError:
        return "Error: Failed to set network details."

class NetworkSettingsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set window properties
        self.setWindowTitle('Network Settings')
        self.setGeometry(100, 100, 400, 300)

        # Create labels and input fields for network parameters
        ip_label = QLabel('IP Address:')
        self.ip_textbox = QLineEdit()
        subnet_mask_label = QLabel('Subnet Mask:')
        self.subnet_mask_textbox = QLineEdit()
        gateway_label = QLabel('Gateway:')
        self.gateway_textbox = QLineEdit()
        dns_label = QLabel('DNS Servers (separated by commas):')
        self.dns_textbox = QLineEdit()

        # Create a button to update network details
        set_button = QPushButton('Set Details')

        # Create a layout and add widgets to it
        layout = QVBoxLayout()
        layout.addWidget(ip_label)
        layout.addWidget(self.ip_textbox)
        layout.addWidget(subnet_mask_label)
        layout.addWidget(self.subnet_mask_textbox)
        layout.addWidget(gateway_label)
        layout.addWidget(self.gateway_textbox)
        layout.addWidget(dns_label)
        layout.addWidget(self.dns_textbox)
        layout.addWidget(set_button)

        # Set the layout for the main window
        self.setLayout(layout)

        # Connect button click event to the set_network_details function
        set_button.clicked.connect(self.set_network_details)

    def set_network_details(self):
        ip_address = self.ip_textbox.text()
        subnet_mask = self.subnet_mask_textbox.text()
        gateway = self.gateway_textbox.text()
        dns_servers = self.dns_textbox.text().split(',')

        result = set_network_details(ip_address, subnet_mask, gateway, dns_servers)
        self.show_message(result)

    def show_message(self, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Network Settings")
        msg_box.setText(message)
        msg_box.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme='light_orange.xml')
    window = NetworkSettingsWindow()
    window.show()
    sys.exit(app.exec_())
