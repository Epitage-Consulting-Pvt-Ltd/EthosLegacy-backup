import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow ,QPushButton , QLineEdit, QCheckBox
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QTimer, QDateTime
from datetime import datetime
from utilities.components import *


class commsExt(QMainWindow):
    def __init__(self):
        super().__init__()

        self.width = 480
        self.height = 800
        self.resize(480, 800)

        self.background_image = QLabel(self)
        self.background_image.setPixmap(QPixmap("images/background.png"))
        self.background_image.setGeometry(0, 0, self.width, self.height)
        self.setWindowFlag(Qt.FramelessWindowHint)

        self.extComm = imgbutton2(self, "images/icons/ExtComm50x50.png", 50, 50, [215, 34], self.close)
        self.extComm.setEnabled(False)

        self.backbtnv2 = imgbutton2(self, "images/icons/BackIcon.png", 30, 30, (5, 44), self.openCommsMan)

        cancel_btn = imgbutton2(self, "images/icons/Cancel_btn.png", 85, 35, [147, 729], self.close)

        ok_btn = imgbutton2(self, "images/icons/OK_btn.png", 85, 35, [248, 729], self.close)

        #labels & textfields

        label = QLabel("Server IP", self)
        label.setStyleSheet("color: #808080")
        label.move(18, 103)

        self.ServerIP_field = QLineEdit(self)
        self.ServerIP_field.setFixedSize(345, 30)
        self.ServerIP_field.move(118, 98)

        label = QLabel("Server Name", self)
        label.setStyleSheet("color: #808080")
        label.move(18, 141)

        self.ServName = QLineEdit(self)
        self.ServName.setFixedSize(345, 30)
        self.ServName.move(118, 136)

        label = QLabel("Database", self)
        label.setStyleSheet("color: #808080")
        label.move(18, 179)

        self.DbNamefield = QLineEdit(self)
        self.DbNamefield.setFixedSize(345, 30)
        self.DbNamefield.move(118, 174)

        label = QLabel("User ID", self)
        label.setStyleSheet("color: #808080")
        label.move(18, 217)

        self.UID_textfield = QLineEdit(self)
        self.UID_textfield.setFixedSize(345, 30)
        self.UID_textfield.move(118, 212)

        label = QLabel("Password", self)
        label.setStyleSheet("color: #808080")
        label.move(18, 255)

        self.password_field = QLineEdit(self)
        self.password_field.setEchoMode(QLineEdit.Password)
        self.password_field.setFixedSize(345, 30)
        self.password_field.move(118, 250)

        label = QLabel("Mesh User ID", self)
        label.setStyleSheet("color: #808080")
        label.move(18, 293)

        self.meshUID_field = QLineEdit(self)
        self.meshUID_field.setFixedSize(345, 30)
        self.meshUID_field.move(118, 288)

        label = QLabel("Mesh PWD", self)
        label.setStyleSheet("color: #808080")
        label.move(18, 331)

        self.meshPWD_field = QLineEdit(self)
        self.meshPWD_field.setFixedSize(345, 30)
        self.meshPWD_field.move(118, 326)


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

    def openCommsMan(self):
        from CommsManagement import comm_man
        self.openCommsMan = comm_man()
        self.openCommsMan.show()
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
    window = commsExt()
    window.show()
    sys.exit(app.exec_())