import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow ,QPushButton , QLineEdit
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QTimer, QDateTime
from datetime import datetime
from utilities.components import *


class edit_time_slots(QMainWindow):
    def __init__(self):
        super().__init__()

        self.width = 480
        self.height = 800
        self.resize(480, 800)

        self.background_image = QLabel(self)
        self.background_image.setPixmap(QPixmap("images/background.png"))
        self.background_image.setGeometry(0, 0, self.width, self.height)
        self.setWindowFlag(Qt.FramelessWindowHint)

        edit_slot = imgbutton2(self, "images/icons/editTimeSlot.png", 50, 50, [215, 34], self.close)

        cancel_btn = imgbutton2(self, "images/icons/Cancel_btn.png", 85, 35, [147, 729], self.close)

        ok_btn = imgbutton2(self, "images/icons/OK_btn.png", 85, 35, [248, 729], self.close)

        self.backbtnv2 = imgbutton2(self, "images/icons/BackIcon.png", 30, 30, (5, 44), self.openTimeSlot)

        #labels & textfields

        label = QLabel("Slot ID", self)
        label.setStyleSheet("color: #808080")
        label.move(18, 102)

        self.slotID_field = QLineEdit(self)
        self.slotID_field.setFixedSize(355, 30)
        self.slotID_field.move(108, 96)

        label = QLabel("Slot Name", self)
        label.setStyleSheet("color: #808080")
        label.move(18, 139)

        self.slotName_field = QLineEdit(self)
        self.slotName_field.setFixedSize(355, 30)
        self.slotName_field.move(108, 134)

        label = QLabel("From Time", self)
        label.setStyleSheet("color: #808080")
        label.move(18, 176)

        self.fromTime_field = QLineEdit(self)
        self.fromTime_field.setFixedSize(130, 30)
        self.fromTime_field.move(108, 171)

        label = QLabel("To Time", self)
        label.setStyleSheet("color: #808080")
        label.move(257, 177)

        self.toTime_field = QLineEdit(self)
        self.toTime_field.setFixedSize(130, 30)
        self.toTime_field.move(333, 172)

    #first row

        label = QLabel("Menu ID", self)
        label.setStyleSheet("color: #808080")
        label.move(18, 225)

        self.menuID_field = QLineEdit(self)
        self.menuID_field.setFixedSize(60, 30)
        self.menuID_field.move(108, 219)

        label = QLabel("Menu Name", self)
        label.setStyleSheet("color: #808080")
        label.move(178, 224)

        self.menuName_field = QLineEdit(self)
        self.menuName_field.setFixedSize(155, 30)
        self.menuName_field.move(268, 219)

    #second row

        label = QLabel("Menu ID", self)
        label.setStyleSheet("color: #808080")
        label.move(18, 263)

        self.menuID_field = QLineEdit(self)
        self.menuID_field.setFixedSize(60, 30)
        self.menuID_field.move(108, 257)

        label = QLabel("Menu Name", self)
        label.setStyleSheet("color: #808080")
        label.move(178, 262)

        self.menuName_field = QLineEdit(self)
        self.menuName_field.setFixedSize(155, 30)
        self.menuName_field.move(268, 257)

    #third row

        label = QLabel("Menu ID", self)
        label.setStyleSheet("color: #808080")
        label.move(18, 301)

        self.menuID_field = QLineEdit(self)
        self.menuID_field.setFixedSize(60, 30)
        self.menuID_field.move(108, 295)

        label = QLabel("Menu Name", self)
        label.setStyleSheet("color: #808080")
        label.move(178, 300)

        self.menuName_field = QLineEdit(self)
        self.menuName_field.setFixedSize(155, 30)
        self.menuName_field.move(268, 295)


        # Create label for date and time
        self.date_time_label = QLabel(self)
        self.date_time_label.setGeometry(5, 4, 190, 20)

        # Set font for date and time label
        font_small = QFont("inika", 10, QFont.Normal)
        self.date_time_label.setFont(font_small)

        # Create label for time
        self.time_label = QLabel(self)
        self.time_label.setGeometry(195, 547, 300, 30)
        self.time_label.setFont(font_small)

        # Update date and time every second
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_date_time)
        self.timer.start(1000)

        # Initial date and time display
        self.update_date_time()

    def openTimeSlot(self):
        from TimeSlots import time_slots
        self.openTimeSlot = time_slots()
        self.openTimeSlot.show()
        self.close()

    def update_date_time(self):
        # Get current date and time
        current_datetime = datetime.now()

        # Format the date as "14th June 2023"
        formatted_date = current_datetime.strftime("%d{} %B %Y").format(
            "th" if 10 <= current_datetime.day <= 19 else
            {1: "st", 2: "nd", 3: "rd"}.get(current_datetime.day % 10, "th")
        )

        # Get the current day
        current_day = current_datetime.strftime("%A")

        # Format the time as "hh:mm:ss"
        formatted_time = current_datetime.strftime("%H:%M:%S")

        # Update date and time labels
        current_datetime_str = f"{formatted_date} - {formatted_time}"
        self.date_time_label.setText(current_datetime_str)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = edit_time_slots()
    window.show()
    sys.exit(app.exec_())