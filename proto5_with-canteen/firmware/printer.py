from escpos.printer import Serial
import time
from datetime import datetime


class Printer:
    def __init__(self):
        self.printer = Serial(
            devfile="/dev/serial0",
            baudrate=9600,
            bytesize=8,
            parity="N",
            stopbits=1,
            timeout=3000.00,
            dsrdtr=True,
        )

        self.printer.set(
            align="left",
            font="a",
            width=1,
            height=1,
            density=5,
            smooth=False,
            flip=False,
        )

    def print_employee(self, employee):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        printer_text = (
            f"E_ID: {employee['EmployeeID']}\n"
            f"E_Name: {employee['EmployeeName']}\n"
            f"Timestamp: {current_time}"
        )

        with self.printer as printer:
            printer.text(printer_text)
            printer.cut("PART")

        time.sleep(1)
