## Verification for card and finger
## THIS CODE IS USED TO VERIFY THE USER USING CARD 1ST AND THEN FINGER  

import sqlite3
from time import sleep
from mfrc522 import SimpleMFRC522
from infrastructure.database.repository.employee_repository import EmployeeRepository
from firmware.led import LEDStripController
from utilities.popup_example import MainWindow, PopupDialog
from PyQt5.QtCore import QTimer, QObject, pyqtSignal
from firmware.fps_verify import VerifyFingerprint
from firmware.fps_main import Fingerprint
import threading
import RPi.GPIO as GPIO

class Signal_manager(QObject):
    rfid_id = pyqtSignal(int)

class RFIDReader:
    def __init__(self):
        self.employee_repository = EmployeeRepository()
        self.reader = SimpleMFRC522()
        self.set_led = LEDStripController()
        self.popup_dialogue = MainWindow()
        self.verify_finger = VerifyFingerprint(db_path='infrastructure/database/ethos_firmware.db')
        self.f = Fingerprint('/dev/ttyUSB0', 115200)
        self.verify_id = Signal_manager()
        self.fps_id = None
        self.read_thread = None
        self.thread_stop_event = threading.Event()  # Ensure thread stop event is initialized

    ##only card verification
    def scan_rfid(self):
        try:
            while not self.thread_stop_event.is_set():
                print("****Scan your card now")
                rf_id, text = self.reader.read()

                # Verify card from the employee table
                with sqlite3.connect('infrastructure/database/ethos_firmware.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT client_emp_id, emp_id, emp_name FROM employee WHERE rf_id=?", (rf_id,))
                    employee = cursor.fetchone()

                if employee:
                    self.set_led.set_green()
                    client_emp_id, emp_id, emp_name = employee
                    print(f"Employee verified for Card: {emp_name}")
                    sleep(1)
                    self.set_led.set_blue()                    
                    # Turn on fingerprint sensor
                    # self.verify_finger.set_fps_id(rf_id)
                    if self.f.init():
                        fp = self.f.identify()
                        print("Finger scan found:", fp)
                        cursor = conn.cursor()
                        # cursor.execute("SELECT * FROM finger_point_scan WHERE LL=? OR LR=? OR LM=?\
                        #                 OR LI=? OR LT=? OR RL=? OR RR=? OR RM=? OR RI=? OR RT=?", (fp,fp,fp,fp,fp,fp,fp,fp,fp,fp,))
                        cursor.execute("\
                                       SELECT LL, LR, LM, LI, LT, RL, RR, RM, RI, RT\
                                        FROM finger_point_scan\
                                        WHERE emp_id=? AND LL=? OR LR=? OR LM=?\
                                            OR LI=? OR LT=? OR RL=? OR RR=? OR RM=? OR RI=? OR RT=?\
                                        ", (emp_id, fp,fp,fp,fp,fp,fp,fp,fp,fp,fp,))

                        finger = cursor.fetchone()
                        # employee_details = f"Name: {emp_name}\nID: {client_emp_id}\nFingerID: {finger}"
                        print("fp_id found in DB", finger)

                        if finger:
                              # Fingerprint verified, show employee details
                            self.set_led.set_green()
                            emp_finger = None
                            for idx, finger_val in enumerate(finger[2:]):  # Assuming finger[2:] contains the finger data
                                if finger_val:  # Assuming finger_val is True if scanned
                                    # Determining the finger based on the index of the column (0 indexed)
                                    if idx == 0:
                                        emp_finger = 'LL'
                                    elif idx == 1:
                                        emp_finger = 'LR'
                                    elif idx == 2:
                                        emp_finger = 'LM'
                                    elif idx == 3:
                                        emp_finger = 'LI'
                                    elif idx == 4:
                                        emp_finger = 'LT'
                                    elif idx == 5:
                                        emp_finger = 'RL'
                                    elif idx == 6:
                                        emp_finger = 'RR'
                                    elif idx == 7:
                                        emp_finger = 'RM'
                                    elif idx == 8:
                                        emp_finger = 'RI'
                                    elif idx == 9:
                                        emp_finger = 'RT'
                                    break  # Exit loop once finger is determined

                            # Fingerprint verified, show employee details including finger information
                            if emp_finger:
                                self.set_led.set_green()
                                employee_details_with_finger = f"Name: {emp_name}\nID: {client_emp_id}\nFinger Scanned: {emp_finger}"
                                popup_dialogue = PopupDialog(employee_details_with_finger)
                                popup_dialogue.show()
                                sleep(1)
                                self.set_led.clear_leds()
                                popup_dialogue.accept()
                                self.verify_id.rfid_id.emit(rf_id)
                            else:
                                print("Fingerprint verification failed.")
                                self.set_led.set_red()
                                popup_dialogue = PopupDialog("No Fingerprint found for the Employee!")
                                popup_dialogue.show()
                                sleep(1)
                                self.set_led.clear_leds()
                                popup_dialogue.accept()
                                print("Employee not found.")
                        else:
                            print("Fingerprint verification failed.")
                            self.set_led.set_red()
                            popup_dialogue = PopupDialog("No Fingerprint found for the Employee!")
                            popup_dialogue.show()
                            sleep(2)
                            self.set_led.clear_leds()
                            popup_dialogue.accept()
                            print("Employee not found.")
                    else:
                        print("FPS failed to initiate")
                        popup_dialogue = PopupDialog("We are sorry, Please Try again!")
                        popup_dialogue.show()
                        sleep(5)
                        self.set_led.clear_leds()
                        popup_dialogue.accept()
                else:
                    self.set_led.set_red()
                    print("Employee not found.")
                    popup_dialogue = PopupDialog("No information found!")
                    popup_dialogue.show()
                    sleep(1)
                    self.set_led.clear_leds()
                    popup_dialogue.accept()
                    print("Employee not found.")

                sleep(1)

        except KeyboardInterrupt:
            print("KeyboardInterrupt detected. Cleaning up.")
            self.cleanup_rfid()
            raise

    def start_reading_thread(self):
        self.read_thread = threading.Thread(target=self.scan_rfid)
        self.read_thread.start()
        return self.read_thread

    def wait_for_read_thread(self):
        if self.read_thread:
            self.read_thread.join()

    def cleanup_rfid(self):
        try:
            if self.read_thread:
                self.thread_stop_event.set()
                self.read_thread.join()
        finally:
            print("Cleanup completed.")