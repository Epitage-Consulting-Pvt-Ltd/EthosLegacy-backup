import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QMessageBox

# Function to get the current Ethernet details
def get_ethernet_details():
    try:
        output = subprocess.check_output(['ip', 'addr', 'show', 'dev', 'eth0']).decode()
        return output
    except subprocess.CalledProcessError:
        return "Error: Failed to retrieve Ethernet details."

# Function to get the current Wi-Fi details
def get_wifi_details():
    try:
        output = subprocess.check_output(['nmcli', '-f', 'SSID', 'device', 'wifi']).decode()
        return output
    except subprocess.CalledProcessError:
        return "Error: Failed to retrieve Wi-Fi details."

# Function to set the Ethernet details
def set_ethernet_details(ip_address, subnet_mask, gateway, dns_servers):
    try:
        subprocess.check_output(['sudo', 'ip', 'addr', 'flush', 'dev', 'eth0'])
        subprocess.check_output(['sudo', 'ip', 'addr', 'add', ip_address + '/' + subnet_mask, 'dev', 'eth0'])
        subprocess.check_output(['sudo', 'ip', 'route', 'del', 'default'])
        subprocess.check_output(['sudo', 'ip', 'route', 'add', 'default', 'via', gateway])
        with open('/etc/resolv.conf', 'w') as file:
            for dns_server in dns_servers:
                file.write('nameserver ' + dns_server + '\n')
        return "Success: Ethernet details updated."
    except subprocess.CalledProcessError:
        return "Error: Failed to set Ethernet details."

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
        self.setGeometry(100, 100, 480, 800)

        # Create labels and input fields for Ethernet parameters
        eth_label = QLabel('Ethernet Details:')
        ip_label = QLabel('IP Address:')
        subnet_mask_label = QLabel('Subnet Mask:')
        gateway_label = QLabel('Gateway:')
        dns_label = QLabel('DNS Servers (separated by commas):')

        self.ip_textbox = QLineEdit()
        self.subnet_mask_textbox = QLineEdit()
        self.gateway_textbox = QLineEdit()
        self.dns_textbox = QLineEdit()

        # Create labels and input fields for Wi-Fi parameters
        wifi_label = QLabel('Wi-Fi Details:')
        ssid_label = QLabel('SSID:')
        password_label = QLabel('Password:')

        self.ssid_textbox = QLineEdit()
        self.password_textbox = QLineEdit()
        self.password_textbox.setEchoMode(QLineEdit.Password)

        # Create buttons for getting and setting network details
        get_eth_button = QPushButton('Get Ethernet Details')
        get_wifi_button = QPushButton('Get Wi-Fi Details')
        set_eth_button = QPushButton('Set Ethernet Details')
        set_wifi_button = QPushButton('Set Wi-Fi Details')

        # Create text boxes to display retrieved details
        self.eth_details_textbox = QTextEdit()
        self.eth_details_textbox.setReadOnly(True)
        self.wifi_details_textbox = QTextEdit()
        self.wifi_details_textbox.setReadOnly(True)

        # Create layouts for Ethernet and Wi-Fi parameters
        eth_layout = QVBoxLayout()
        eth_layout.addWidget(ip_label)
        eth_layout.addWidget(self.ip_textbox)
        eth_layout.addWidget(subnet_mask_label)
        eth_layout.addWidget(self.subnet_mask_textbox)
        eth_layout.addWidget(gateway_label)
        eth_layout.addWidget(self.gateway_textbox)
        eth_layout.addWidget(dns_label)
        eth_layout.addWidget(self.dns_textbox)
        eth_layout.addWidget(set_eth_button)

        wifi_layout = QVBoxLayout()
        wifi_layout.addWidget(ssid_label)
        wifi_layout.addWidget(self.ssid_textbox)
        wifi_layout.addWidget(password_label)
        wifi_layout.addWidget(self.password_textbox)
        wifi_layout.addWidget(set_wifi_button)

        # Create main layout for the window
        layout = QVBoxLayout()
        layout.addWidget(eth_label)
        layout.addLayout(eth_layout)
        layout.addWidget(get_eth_button)
        layout.addWidget(self.eth_details_textbox)
        layout.addWidget(wifi_label)
        layout.addLayout(wifi_layout)
        layout.addWidget(get_wifi_button)
        layout.addWidget(self.wifi_details_textbox)

        # Set the layout for the main window
        self.setLayout(layout)

        # Connect button click events to functions
        get_eth_button.clicked.connect(self.get_ethernet_details)
        get_wifi_button.clicked.connect(self.get_wifi_details)
        set_eth_button.clicked.connect(self.set_ethernet_details)
        set_wifi_button.clicked.connect(self.set_wifi_details)

    def get_ethernet_details(self):
        details = get_ethernet_details()
        self.eth_details_textbox.setText(details)

    def get_wifi_details(self):
        details = get_wifi_details()
        self.wifi_details_textbox.setText(details)

    def set_ethernet_details(self):
        ip_address = self.ip_textbox.text()
        subnet_mask = self.subnet_mask_textbox.text()
        gateway = self.gateway_textbox.text()
        dns_servers = self.dns_textbox.text().split(',')

        result = set_ethernet_details(ip_address, subnet_mask, gateway, dns_servers)
        self.show_message(result)

    def set_wifi_details(self):
        ssid = self.ssid_textbox.text()
        password = self.password_textbox.text()

        result = set_wifi_details(ssid, password)
        self.show_message(result)

    def show_message(self, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Network Settings")
        msg_box.setText(message)
        msg_box.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = NetworkSettingsWindow()
    window.show()
    sys.exit(app.exec_())
