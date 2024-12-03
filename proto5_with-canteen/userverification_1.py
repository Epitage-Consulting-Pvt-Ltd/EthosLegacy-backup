import sys
import csv
import logging
import time
import codecs
import signal
import serial
import RPi.GPIO as GPIO
import sqlite3

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton
from PyQt5.QtGui import QFont
from mfrc522 import SimpleMFRC522
from fps import Fingerprint
from utilities.themeV3 import BUTTON_STYLE
from card_verifier import CardVerifier


# Initialize Fingerprint object
f = Fingerprint("/dev/ttyUSB0", 9600)

class CardVerificatiion(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize RFID reader
        self.rfid_reader = SimpleMFRC522()

        # Set window size
        self.window_width = 480
        self.window_height = 800
        self.setGeometry(0, 0, self.window_width, self.window_height)
        self.setWindowFlag(Qt.FramelessWindowHint)

        # Set window title
        self.setWindowTitle("User Verification")

        # Add 'Back' button
        self.back_btn = QPushButton('Back', self)
        self.back_btn.move(10, 10)
        self.back_btn.clicked.connect(self.show_menu_grid_window)
        self.back_btn.clicked.connect(self.close)
        self.back_btn.setStyleSheet(BUTTON_STYLE)

        # Create label to display user details
        self.user_label = QLabel("Scan RFID card", self)
        self.user_label.setGeometry(100, 150, 280, 60)
        self.user_label.setAlignment(Qt.AlignCenter)
        self.user_label.setFont(QFont("Arial", 14))

        # Create verify button
        self.verify_button = QPushButton("Verify Card", self)
        self.verify_button.setGeometry(100, 100, 280, 60)
        self.verify_button.clicked.connect(self.verify_class)

        verify_fps = QPushButton("Verify Finger", self)
        verify_fps.clicked.connect(self.verify)
        verify_fps.setGeometry(100, 300, 280, 60)


        self.user_label1 = QLabel("Scan your finger", self)
        self.user_label1.setGeometry(100, 350, 280, 60)
        self.user_label1.setAlignment(Qt.AlignCenter)
        self.user_label1.setFont(QFont("Arial", 14))

        #Create timer for resetting the verify button
        self.reset_timer = QTimer()
        self.reset_timer.timeout.connect(self.reset_button)

    # def verify_card(self):
    #     try:
    #         # Prompt user to scan RFID card
    #         self.user_label.setText("Place RFID card on reader or press Ctrl+C to cancel.")
    #         rfid_id = self.rfid_reader.read_id()
    #
    #         # Check if RFID card is associated with a user in the CSV file
    #         with open("data/EmpMaster-Epitage.csv", "r") as file:
    #             reader = csv.reader(file)
    #             for row in reader:
    #                 if row[3] == str(rfid_id):
    #                     # User found
    #                     self.user_label.setText("Verified user with ID: " + row[1] + row[2])
    #                     break
    #             else:
    #                 # User not found
    #                 self.user_label.setText("Access denied.")
    #
    #         # Start the timer for button reset
    #         self.reset_timer.start(5000)  # 30 seconds
    #
    #     except KeyboardInterrupt:
    #         # User cancelled operation
    #         self.user_label.setText("Operation cancelled.")
    #
    #     except Exception as e:
    #         # Error occurred
    #         self.user_label.setText("Error: " + str(e))
    #
    def verify_class(self):
        from card_verifier import CardVerifier
        self.verify_class = CardVerifier()
        self.verify_class.show()

        # global verifier
        # try:
        #     # Prompt user to scan RFID card
        #     self.user_label.setText("Place RFID card on reader or press Ctrl+C to cancel.")
        #     rfid_id = self.rfid_reader.read_id()
        #
        #     # Use the CardVerifier class to verify the card
        #     verifier = CardVerifier("employee_data.db")
        #     result = verifier.verify_card(rfid_id)
        #
        #     if result:
        #         # User found
        #         employee_id, employee_name, timestamp = result[0]["EmployeeID"], result[0]["EmployeeName"], result[0][
        #             "timestamp"]
        #         self.user_label.setText(
        #             f"Verified user: ID - {employee_id}, Name - {employee_name}, Timestamp - {timestamp}")
        #     else:
        #         # User not found
        #         self.user_label.setText("Access denied.")
        #
        #     # Start the timer for button reset
        #     self.reset_timer.start(5000)  # 5 seconds
        #
        # except KeyboardInterrupt:
        #     # User canceled operation
        #     self.user_label.setText("Operation cancelled.")
        #
        # except Exception as e:
        #     # Error occurred
        #     self.user_label.setText("Error: " + str(e))
        # finally:
        #     verifier.disconnect()  # Disconnect from the database

    def verify(self):
        idtemp = f.identify()
        if f.capture_finger():  # capture_finger function
            if idtemp == -1:
                GPIO.output(11, GPIO.HIGH)
                #print("You are not recognized!")
                self.user_label1.setText("Invalid User")

            else:
                GPIO.output(12, GPIO.HIGH)
                #print("Verified! User ID: %d" % idtemp)
                self.user_label1.setText("Verified!! User  ID: %d" % idtemp)
        else:
            print("Failed to capture finger.")

        time.sleep(2)
        GPIO.output(11, GPIO.LOW)
        GPIO.output(12, GPIO.LOW)

    def reset_button(self):
        # Reset the verify button and label
        self.user_label.setText("Scan an RFID card")
        self.verify_button.setEnabled(True)

    def closeEvent(self, event):
        # Close the connection to the RFID reader
        GPIO.cleanup()
        event.accept()

    def show_menu_grid_window(self):
        from MenuScreenV4 import MenuWindow #opens previous page upon pressing back button
        self.menu_grid_window = MenuWindow()
        self.menu_grid_window.show()

if __name__ == "__main__":
    # Initialize the fingerprint sensor
    if f.init():
        print("Fingerprint sensor initialized.")
    else:
        print("Failed to initialize fingerprint sensor.")
        sys.exit(1)

    # Initialize the PyQt application
    app = QApplication(sys.argv)

    # Create the main window
    window = CardVerificatiion()
    window.show()

    # Run the application event loop
    sys.exit(app.exec_())
