import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow ,QPushButton , QLineEdit
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QTimer, QDateTime
from datetime import datetime
from utilities.components import *


class comm_man(QMainWindow):
    def __init__(self):
        super().__init__()

        self.width = 480
        self.height = 800
        self.resize(480, 800)

        self.background_image = QLabel(self)
        self.background_image.setPixmap(QPixmap("images/background.png"))
        self.background_image.setGeometry(0, 0, self.width, self.height)
        self.setWindowFlag(Qt.FramelessWindowHint)

        commsInt = imgbutton2(self, "images/icons/CommsInt100x100.png", 100, 100, [18, 141], self.openIntComm)

        commsExt = imgbutton2(self, "images/icons/CommsExt100x100.png", 100, 100, [134, 141], self.openExtComm)

        self.backbtnv2 = imgbutton2(self, "images/icons/BackIcon.png", 30, 30, (5, 44), self.openUserMenu)

        self.commsMain = imgbutton2(self, "images/icons/Comms50x50.png", 50, 50, [215, 34], self.close)
        self.commsMain.setEnabled(False)

        label = QLabel("Password", self)
        label.setStyleSheet("color: #808080")
        label.move(18, 106)

        # Create the password field
        self.password_field = QLineEdit(self)
        self.password_field.setPlaceholderText("here")
        self.password_field.setEchoMode(QLineEdit.Password)
        self.password_field.setFixedSize(355, 30)
        self.password_field.move(108, 101)

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

    def openIntComm(self):
        from commsInternals import commsInt
        self.openIntComm = commsInt()
        self.openIntComm.show()
        self.close()

    def openExtComm(self):
        from commsExternal import commsExt
        self.openExtComm = commsExt()
        self.openExtComm.show()
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

    def openUserMenu(self):
        from MenuScreenV4 import MenuWindow
        self.openMenu = MenuWindow()
        self.openMenu.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = comm_man()
    window.show()
    sys.exit(app.exec_())
