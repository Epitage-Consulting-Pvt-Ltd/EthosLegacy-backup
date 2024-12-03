# import sqlite3
from sqliteInterface import SQLiteInterface
from mfrc522 import SimpleMFRC522
from escpos.printer import Serial
from datetime import datetime
import board
import neopixel
import time
import RPi.GPIO as GPIO
import sqlite3
# from rfid_reader import RFIDReader
import threading
import pygame as pg
white = (255, 255, 255)
blue = (0, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)


class RFIDDatabaseOperations:
    def __init__(self):
        # Initialize the SQLite database and other resources
        # self.db_name = "employee_data.db"
        # self.db = SQLiteInterface(self.db_name)
        # self.db.connect()
        # GPIO.setmode(GPIO.BCM)
        self.is_running = False
        self.thread = None
        self.reader = None

    def start_operations(self):
        if not self.is_running:
            self.is_running = True
            self.thread = threading.Thread(target=self.run_operations)
            self.thread.start()
            print("Run operations thread started.")

    def stop_operations(self):
        if self.is_running:
            self.is_running = False
            self.thread.join()
            # if self.reader is not None:
            # self.reader = SimpleMFRC522()
            # self.reader.close_sensor()     
            GPIO.cleanup()  # Clean up GPIO pins
            print("Run operations thread stopped.")    
    
    def run_operations(self):
        self.reader = SimpleMFRC522()
        try:
            def set_all_leds(color):
                LED_COUNT = 8  # Number of LEDs in your strip
                LED_PIN = board.D12  # GPIO pin where your data line is connected
                ORDER = neopixel.GRB  # Color order of your strip (GRB for WS2812B)
                # Create NeoPixel object
                strip = neopixel.NeoPixel(LED_PIN, LED_COUNT, auto_write=False, pixel_order=ORDER)

                for i in range(LED_COUNT):
                    strip[i] = color
                strip.show()

            while self.is_running:
                print("Running RFID operations...")
                # Initialize the SQLite database
                db_name = "infrastructure/database/ethos_firmware.db"
                db = SQLiteInterface(db_name)
                db.connect()
                rf_id, text = self.reader.read()

                # Initialize Printer
                printer = Serial(devfile='/dev/serial0',
                                 baudrate=9600,
                                 bytesize=8,
                                 parity='N',
                                 stopbits=1,
                                 timeout=3000.00,
                                 dsrdtr=True)

                # Scan the RFID card
                print("Place an RFID card near the reader...")
                print(f"Scanned RFID Card ID: {rf_id}")
                with sqlite3.connect('infrastructure/database/ethos_firmware.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT client_emp_id, emp_id, emp_name FROM employee WHERE rf_id=?", (rf_id,))
                    employee = cursor.fetchone()
                # Get the current timestamp
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print("Result of SQL Query:", employee)

                if employee:
                    client_emp_id, emp_id, emp_name = employee
                    # client_emp_id, emp_id, emp_name = result
                    print("Employee found:")
                    print(f"Employee ID: {emp_name}")
                    print(f"Employee Name: {client_emp_id}")
                    print(f"Employee Name: {emp_id}")
                    # print(f"Timestamp: {employee['timestamp']}")
                    set_all_leds(green)
                    freq = 44100    # audio CD quality
                    bitsize = -16   # unsigned 16 bit
                    channels = 2    # 1 is mono, 2 is stereo
                    buffer = 2048   # number of samples (experiment to get right sound)
                    pg.mixer.init(freq, bitsize, channels, buffer)
                    # optional volume 0 to 1.0
                    pg.mixer.music.set_volume(1.0)


                    # Load the MP3 file
                    pg.mixer.music.load('thank-you-168416.mp3')

                    # Play the audio file
                    pg.mixer.music.play()

                    # Print the employee details to the thermal printer
                    printer.set(
                        align="left",
                        font="a",
                        width=1,
                        height=1,
                        density=5,
                        smooth=False,
                        flip=False
                    )
                    # printer.image("/home/pi2/Device_V0.0/DB/Piaggio1.png", high_density_vertical=True,
                    #               high_density_horizontal=True, impl="bitImageColumn")
                    printer.text(f"E_ID: {client_emp_id}\n")
                    printer.text(f"E_Name: {emp_name}\n")
                    # printer.text(f"Timestamp: {employee['timestamp']}")
                    printer.text(f"Timestamp: {current_time}")
                    # printer.set_text_size(1, 1)
                    printer.cut('PART')
                    time.sleep(1)
                    set_all_leds((0, 0, 0))

                else:
                    print("Employee not found in the database.")
                    set_all_leds(red)
                    time.sleep(1)
                    set_all_leds((0, 0, 0))
                time.sleep(1)

        except KeyboardInterrupt:
            # Cleanup operations here
            self.db.disconnect()
            print("Error scanning RFID card:", e)
            GPIO.cleanup()
            raise()
            # pass
        
        GPIO.cleanup()
        # finally:
        #     # Disconnect from the database and close resources here
        #     self.db.disconnect()
        #     # Close the printer connection
        #     # Other cleanup operations


if __name__ == "__main__":
    rfid_db_operations = RFIDDatabaseOperations()
    rfid_db_operations.run_operations()
    # rfid_db_operations = RFIDDatabaseOperations()
    # print(f"RFID Database Operations object: {rfid_db_operations}")
    # try:
    #     rfid_db_operations.run_operations()
    # except KeyboardInterrupt:
    #     rfid_db_operations.end_operation()