import sys

from PyQt5.QtCore import QDateTime ,Qt
from PyQt5.QtGui import QPixmap, QPalette
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout

# from theme import WINDOW_BACKGROUND_COLOR, \
#    RFID_WINDOW_FOREGROUND_COLOR


class RFIDPromptDummy(QWidget):
    def __init__(self, company_pic ,employee_name, employee_picture):
        super().__init__()

        # set window size
        self.setFixedSize(200, 400)

        # Set window background and foreground colors
        palette = self.palette()
        palette.setColor(QPalette.Window, WINDOW_BACKGROUND_COLOR)
        palette.setColor(QPalette.WindowText, RFID_WINDOW_FOREGROUND_COLOR)
        self.setPalette(palette)

        # create QLabel for company picture
        company_pic_label = QLabel(self)
        pixmap = QPixmap(company_pic)
        company_pic_label.setPixmap(pixmap.scaledToWidth(150))

        # create QLabel for employee picture
        employee_pic_label = QLabel(self)
        pixmap = QPixmap(employee_picture)
        employee_pic_label.setPixmap(pixmap.scaledToWidth(150))

        # create QLabel for employee name
        employee_name_label = QLabel(employee_name, self)
        employee_name_label.setAlignment(Qt.AlignCenter)

        # create QLabel for timestamp
        timestamp = QDateTime.currentDateTime().toString("MMM dd, yyyy hh:mm:ss AP")
        timestamp_label = QLabel(f"Timestamp: {timestamp}", self)
        timestamp_label.setWordWrap(True)

        # Punch has been apporved

        # create QVBoxLayout and add widgets to it
        vbox = QVBoxLayout()
        vbox.addWidget(employee_pic_label)
        vbox.addWidget(employee_name_label)
        vbox.addWidget(timestamp_label)

        # set layout for the window
        self.setLayout(vbox)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RFIDPromptDummy("sudarshanlogo.png","Rajesh Peche", "Epitage.png")
    window.show()
    sys.exit(app.exec_())
