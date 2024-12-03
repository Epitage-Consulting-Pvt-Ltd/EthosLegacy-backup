import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow ,QPushButton , QLineEdit
from PyQt5.QtGui import QPixmap, QFont, QIcon
from PyQt5.QtCore import Qt, QTimer, QDateTime
from datetime import datetime
from utilities.components import *


class togButton(QMainWindow):
    def __init__(self):
        super().__init__()

        self.width = 480
        self.height = 800
        self.resize(480, 800)

        self.background_image = QLabel(self)
        self.background_image.setPixmap(QPixmap("images/background.png"))
        self.background_image.setGeometry(0, 0, self.width, self.height)

        self.Crd_but = QPushButton(self)
        self.Crd_but.setGeometry(17, 246, 100, 100)
        self.Crd_but.setCheckable(True)
        self.Crd_but.clicked.connect(self.crd_tog)
        icon = QIcon("images/icons/Card.png")
        self.Crd_but.setIcon(icon)
        icon_size = QSize(90, 90)
        self.Crd_but.setIconSize(icon_size)

        self.finger_but = QPushButton(self)
        self.finger_but.setGeometry(17, 372, 100, 100)
        self.finger_but.setCheckable(True)
        self.finger_but.clicked.connect(self.fing_tog)
        icon = QIcon("images/icons/FingerVeri_Icon.png")
        self.finger_but.setIcon(icon)
        icon_size = QSize(90, 90)
        self.finger_but.setIconSize(icon_size)


    def crd_tog(self):
        if self.Crd_but.isChecked():

            self.Crd_but.setStyleSheet("QPushButton {background-color:lightgreen}")

        else:

            self.Crd_but.setStyleSheet("QPushButton {background-color:lightcoral}")

    def fing_tog(self):
            if self.finger_but.isChecked():

                self.finger_but.setStyleSheet("QPushButton {background-color:lightgreen}")

            else:

                self.finger_but.setStyleSheet("QPushButton {background-color:lightcoral}")



        #self.canteen = imgbutton2(self, "images/icons/Card.png", 100, 100, [17, 246], self.close)
        #self.canteen.setCheckable(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = togButton()
    window.show()
    sys.exit(app.exec_())
