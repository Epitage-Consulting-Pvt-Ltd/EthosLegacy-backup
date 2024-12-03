# TODO: Code not required, need to remove
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QWidget
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QTimer
from datetime import datetime

class DateTimeWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Create date and time labels
        self.date_time_label = self.createDateTimeLabel(geometry=(5, 4, 190, 20), font_size=10)
        self.time_label = self.createDateTimeLabel(geometry=(195, 547, 300, 30), font_size=10)

        # Update date and time every second
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_date_time)
        self.timer.start(1000)

        # Initial date and time display
        self.update_date_time()

    def createDateTimeLabel(self, geometry=(0, 0, 0, 0), font_size=10):
        label = QLabel(self)
        label.setGeometry(*geometry)
        font = QFont("inika", font_size, QFont.Normal)
        label.setFont(font)
        return label

    def update_date_time(self):
        # Get current date and time
        current_datetime = datetime.now()

        # Format the date as "14th June 2023"
        formatted_date = current_datetime.strftime("%d{} %B %Y").format(
            "th" if 10 <= current_datetime.day <= 19 else
            {1: "st", 2: "nd", 3: "rd"}.get(current_datetime.day % 10, "th")
        )

        # Format the time as "hh:mm:ss"
        formatted_time = current_datetime.strftime("%H:%M:%S")

        # Update date and time labels
        current_datetime_str = f"{formatted_date} - {formatted_time}"
        self.date_time_label.setText(current_datetime_str)
        self.time_label.setText(formatted_time)
