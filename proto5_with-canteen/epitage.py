import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QAction, QMenu, QDialog, QVBoxLayout
from PyQt5.QtGui import QPixmap, QFont, QIcon
from PyQt5.QtCore import Qt, QTimer, QDateTime, QEvent
from datetime import datetime
from utilities.components import create_img_button
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton
import subprocess
import os
from RD_Ops import RFIDDatabaseOperations
from PyQt5.QtCore import QObject, pyqtSignal

class SignalManager(QObject):
    stopThreadAndOpenMenu = pyqtSignal()

class SplashWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window dimensions
        self.width = 480
        self.height = 800
        self.setGeometry(0, 0, self.width, self.height)
        self.setWindowFlag(Qt.FramelessWindowHint)

        self.verify = RFIDDatabaseOperations()
        self.verify.start_operations()
        
        self.signal_manager = SignalManager()
        self.signal_manager.stopThreadAndOpenMenu.connect(self.stopThreadAndOpenMenu)
        
        # Set background image
        self.background_image = QLabel(self)
        self.background_image.setPixmap(QPixmap("images/background.png"))
        self.background_image.setGeometry(0, 0, self.width, self.height)

        # Create label for date and time
        self.date_time_label = QLabel(self)
        self.date_time_label.setGeometry(5, 4, 190, 20)

        # Set font for date and time label
        font_small = QFont("inika", 15, QFont.Bold)
        self.date_time_label.setFont(font_small)

        # Set font for date and time label
        font_big = QFont("inika", 20, QFont.Normal)

        self.logoImage = QLabel(self)
        self.logoImage.setPixmap(QPixmap("images/img.png"))
        self.logoImage.setGeometry(50, 154, 381, 277)

        # Create label for additional date
        self.additional_date_label = QLabel(self)
        self.additional_date_label.setGeometry(50, 509, 380, 26)
        self.additional_date_label.setAlignment(Qt.AlignHCenter)
        self.additional_date_label.setFont(font_small)
        # self.additional_date_label.setAlignment(Qt.AlignVCenter)

        # Create label for time

        self.time_label = QLabel(self)
        self.time_label.setGeometry(205, 547, 300, 30)
        self.time_label.setFont(font_small)

        self.menu_btn = create_img_button(self, 'images/icons/MenuIcon.png', 75, 100, (190, 623), self.openMenuScreen,
                                          "Menu", "#D9D9D9")
        self.menu_btn.installEventFilter(self)

        # Update date and time every second
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_date_time)
        self.timer.start(1000)

        # Initial date and time display
        self.update_date_time()

        # app.installEventFilter(self)
        # Create a button for shutdown and reboot with an image
        self.shutdown_reboot_button = QPushButton(self)
        self.shutdown_reboot_button.setGeometry(5, 44, 30, 30)  # Position and size of the button

        # Load and set the button's image
        image_path = "images/shutdown_button.png"  # Replace with the actual path to your image
        pixmap = QPixmap(image_path)
        self.shutdown_reboot_button.setIcon(QIcon(pixmap))
        self.shutdown_reboot_button.setIconSize(pixmap.size())

        # Remove the rectangular frame and arrow
        self.shutdown_reboot_button.setFlat(True)

        # Set a blank style sheet to remove any potential unwanted styles
        self.shutdown_reboot_button.setStyleSheet("QPushButton { border: none; }")

        # Disable focus indicator and border
        # self.shutdown_reboot_button.setFocusPolicy(Qt.NoFocus)

        # Create a menu with options
        self.menu = QMenu(self)
        self.shutdown_action = QAction("Shutdown", self)
        self.reboot_action = QAction("Reboot", self)

        # Connect actions to their respective functions
        self.shutdown_action.triggered.connect(self.shutdown_device)
        self.reboot_action.triggered.connect(self.reboot_device)

        # Add actions to the menu
        self.menu.addAction(self.shutdown_action)
        self.menu.addAction(self.reboot_action)

        # Connect the menu to the button
        self.shutdown_reboot_button.setMenu(self.menu)

    def eventFilter(self, obj, event):
        if event and hasattr(event, 'type'):
            if obj == self.menu_btn and event is not None and event.type() == QEvent.Type.MouseButtonPress:
                # self.verify.stop_operations()
                self.signal_manager.stopThreadAndOpenMenu.emit()
                return True
        return super().eventFilter(obj, event)

    def shutdown_device(self):
        # Execute the shutdown command
        subprocess.run(["sudo", "shutdown", "-h", "now"])

    def reboot_device(self):
        # Execute the reboot command
        subprocess.run(["sudo", "reboot"])

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
        self.additional_date_label.setText(f"{current_day} , {formatted_date}")
        self.time_label.setText(formatted_time)

    def stopThreadAndOpenMenu(self):
        self.verify.stop_operations()
        self.openMenuScreen()

    def openMenuScreen(self):
        from MenuScreenV4 import MenuWindow
        self.openMenuScreen = MenuWindow()
        self.openMenuScreen.show()
        self.close()
        # test

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SplashWindow()
    window.show()
    sys.exit(app.exec_())