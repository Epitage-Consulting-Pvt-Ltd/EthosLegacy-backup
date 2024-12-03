import sys

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow

from utilities.components import create_img_button, imgbutton ,imgbutton2
from PyQt5.QtCore import Qt, QTimer, QDateTime


class UserWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Set window dimensions
        self.width = 480
        self.height = 800
        self.setGeometry(0, 0, self.width, self.height)
        self.setWindowFlag(Qt.FramelessWindowHint)

        # Set background image
        self.background_image = QLabel(self)
        self.background_image.setPixmap(QPixmap("images/background.png"))
        self.background_image.setGeometry(0, 0, self.width, self.height)

        self.backbtnv2 = imgbutton2(self, "images/icons/BackIcon.png", 30, 30, (5, 44), self.openMenuScreen)

        self.NewUser = create_img_button(self, "images/icons/NewUserIcon.png", 55, 100, (18, 142),
                                         self.openNewUserScreen, "New", "#D9D9D9")
        self.NewUser.setEnabled(True)

        self.EditUser = create_img_button(self, "images/icons/EditUserIcon.png", 55, 100, (133, 142), self.editEmployee,
                                          "Edit", "#D9D9D9")
        self.EditUser.setEnabled(True)

        self.CopyUser = create_img_button(self, "images/icons/CopyUserIcon.png", 55, 100, (248, 142), self.copyEmployee,
                                          "Copy", "#D9D9D9")
        self.CopyUser.setEnabled(True)

        self.DeleteUser = create_img_button(self, "images/icons/DeleteUserIcon.png", 55, 100, (363, 142), self.deleteEmployee,
                                            "Delete", "#D9D9D9")
        self.DeleteUser.setEnabled(True)

    def openNewUserScreen(self):
        from NewUserV4 import EmployeeForm
        self.openNewUserScreen = EmployeeForm()
        self.openNewUserScreen.show()
        self.close()

    def openMenuScreen(self):
        from MenuScreenV4 import MenuWindow
        self.openMenuScreen = MenuWindow()
        self.openMenuScreen.show()
        self.close()

    def editEmployee(self):
        from employeeEdit import EditUserWindow
        self.editEmployee = EditUserWindow()
        self.editEmployee.show()
        self.close()

    def copyEmployee(self):
        pass

    def deleteEmployee(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UserWindow()
    window.show()
    sys.exit(app.exec_())
