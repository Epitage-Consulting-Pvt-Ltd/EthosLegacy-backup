import sys
from PyQt5.QtWidgets import QLabel, QMainWindow, QPushButton, QApplication, QWidget, QVBoxLayout
from PyQt5.QtGui import QPixmap, QFont, QIcon
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from datetime import datetime
from utilities.img_button_text import ImgButtonText
from utilities.img_button import ImgButton
import subprocess
import os
from infrastructure.env_config import EnvConfig


class EthosMainWindow(QWidget):
    dob_line_edit_clicked = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.config = EnvConfig()

        self.current_directory = os.getcwd()
        self.width = 480
        self.height = 800
        self.setGeometry(0, 0, self.width, self.height)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.init_layout()
        self.setup_timer()
        self.update_date_time()

    def setup_timer(self):
        # Update date and time every second
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_date_time)
        self.timer.start(1000)

    def init_layout(self):
        # Set background image
        self.background_image = QLabel(self)
        print("IMAGE_BASE_PATH:", self.config.IMAGE_BASE_PATH)
        self.background_image.setPixmap(QPixmap(os.path.join(self.current_directory, self.config.IMAGE_BASE_PATH + "background.png")))
        self.background_image.setGeometry(0, 0, self.width, self.height)
        # Create label for date and time
        self.date_time_label = QLabel(self)
        # self.date_time_label.setGeometry(5, 4, 190, 20)
        self.date_time_label.setGeometry(5, 4, 140, 20)
        # Set font for date and time label
        font_small = QFont("inika", 15, QFont.Bold)
        self.date_time_label.setFont(font_small)

        self.backbtn = ImgButton(
        self, "BackIcon.png", 30, 30, 30, 30, "#D9D9D9", 5, 44, self.navigate_back)

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
