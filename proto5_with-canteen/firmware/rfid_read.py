# rfid_reader.py
from time import sleep
from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO
import threading
from infrastructure.database.repository.employee_repository import EmployeeRepository
from firmware.led import LEDStripController
# from firmware.play_mp3 import MP3Player
from utilities.popup_example import *
from PyQt5.QtCore import pyqtSignal, QObject, QTimer, Qt
import sqlite3
from PyQt5.QtWidgets import QMessageBox, QApplication
import time
# from firmware.fps_verify import VerifyFingerprint


class Signal_manager(QObject):
    rfid_id = pyqtSignal(int)


class RFIDReader:
    def __init__(self):
        GPIO.setwarnings(False)
        # GPIO.setmode(GPIO.BOARD)
        self.employee_repository = EmployeeRepository()
        self.reader = SimpleMFRC522()
        self.set_led = LEDStripController()
        self.popup_dialogue = MainWindow()
        # self.verify_finger = VerifyFingerprint()
        # self.speaker = MP3Player()
        self.read_thread = None
        self.thread_stop_event = None  # Add this line
        self.id = None
        self.verify_id = Signal_manager()

    ##only card verification
    def scan_rfid(self):
        try:
            conn = sqlite3.connect('infrastructure/database/ethos_firmware.db')
            cursor = conn.cursor()
            # while True:
            while not self.thread_stop_event.is_set():
                # with self.reader as r:
                print("****Scan your card now")
                rf_id, text = self.reader.read()
                cursor.execute("SELECT client_emp_id, emp_name FROM employee WHERE rf_id=?", (rf_id,))
                employee = cursor.fetchone()

                if employee:
                    # Employee found, perform verification actions
                    self.set_led.set_green()
                    client_emp_id, emp_name = employee  # Unpack the tuple
                    employee_details = f"Name: {emp_name}\nID: {client_emp_id}"
                    popup_dialogue = PopupDialog(employee_details, parent=self.popup_dialogue)  # Adjust the parent here
                    popup_dialogue.show()
                    # self.popup_dialogue.show_popup()
                    sleep(1)
                    self.set_led.clear_leds()
                    # self.popup_dialogue.hide()
                    popup_dialogue.accept()
                    self.verify_id.rfid_id.emit(rf_id)
                    sleep(1)

                else:
                    self.set_led.set_red()
                    # self.popup_dialogue.show_popup()
                    popup_dialogue = PopupDialog("Denied!")
                    popup_dialogue.show()
                    sleep(1)
                    self.set_led.clear_leds()
                    # self.popup_dialogue.hide()
                    popup_dialogue.accept()
                #     # self.speaker.play_rejected()
                #     print("Employee not Found")
                    sleep(1)

        except KeyboardInterrupt:
            print("KeyboardInterrupt detected. Cleaning up.")
            # GPIO.cleanup()
            self.cleanup_rfid()
            raise
    
    def start_reading_thread(self):
        self.thread_stop_event = threading.Event()
        self.read_thread = threading.Thread(target=self.scan_rfid)
        self.read_thread.start()
        return self.read_thread

    def wait_for_read_thread(self):
        if self.read_thread:
            self.read_thread.join()

    def get_id(self):
        return self.id
    
    # def cleanup_rfid(self):
    #     """
    #     Stop the fingerprint verification thread.
    #     """
    #     # try:
    #     if self.read_thread:
    #         self.thread_stop_event.set()
    #         self.read_thread.join()
    #     # finally:
    #         GPIO.cleanup()
    #         print("gpio cleanup")

    def cleanup_rfid(self):
        """
        Stop the RFID scanning thread and perform GPIO cleanup.
        """
        try:
            if self.read_thread:
                self.thread_stop_event.set()
                self.read_thread.join()
        finally:
            GPIO.cleanup()
            print("GPIO cleanup completed.")
            