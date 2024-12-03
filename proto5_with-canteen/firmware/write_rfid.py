from PyQt5.QtCore import QThread, pyqtSignal, QObject
from mfrc522 import SimpleMFRC522  # Assuming this is the RFID library you're using
from firmware.led import LEDStripController
from utilities.popup_example import *
import threading
import RPi.GPIO as GPIO

# class Signal_manager(QObject):
#     rfid_scanned = pyqtSignal(int)

class RFIDWrite(QThread):
    rfid_scanned = pyqtSignal(str)  # Define a signal to pass RFID data

    def __init__(self, text):
        super().__init__()
        self.set_led = LEDStripController()
        # self.popup_dialogue = MainWindow()
        self.write_thread = None
        self.thread_stop = None
        self.text = text
        # self.led_controller = None
        self.running = False
        # self.verify_id = Signal_manager()

    def write_rfid(self):
        self.running = True
        try:
            # Perform RFID scanning operation here
            reader = SimpleMFRC522()
            print("Now place your tag to write")
            self.set_led.set_purple()  # Set LED to purple while scanning
            id, text = reader.write(self.text)
            print("Written")
            print("id", id)
            print("text", text)
            print(self.text)
            self.rfid_scanned.emit(str(id))  # Emit the scanned RFID data
        except Exception as e:
            print("Error capturing RFID:", e)
        finally:
            self.set_led.clear_leds()  # Clear LEDs after RFID operation
            self.running = False

    def start_write_thread(self):
        self.thread_stop = threading.Event()
        self.write_thread = threading.Thread(target=self.write_rfid)
        self.write_thread.start()
        return self.write_thread
    
    def wait_for_write_thread(self):
        if self.write_thread:
            self.write_thread.join()

    def cleanup_rfid(self):
        """
        Stop the RFID scanning thread and perform GPIO cleanup.
        """
        # try:
        if self.write_rfid is not None:
            self.thread_stop.set()
            self.write_thread.join()
        # finally:
        GPIO.cleanup()
        print("GPIO cleanup completed.")


