import csv
import sys
import os
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = '/usr/lib/aarch64-linux-gnu/qt5/plugins/'

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QEvent
from PyQt5.QtCore import Qt

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QDialog
from PyQt5.QtWidgets import QCalendarWidget
from PyQt5.QtWidgets import QPushButton, QLineEdit, QComboBox
from PyQt5.uic.properties import QtCore

#from mfrc522 import SimpleMFRC522

#from Register_face import FaceRegistration
#from fps import Fingerprint
from keyboard3 import VirtualKeyboard
from utilities.components import imgbutton, imgbutton2


class imgbutton(QPushButton):
    def __init__(self, parent, image, width, height, position, on_clicked=None):  # Add on_clicked=None with default value
        super().__init__(parent)
        self.image = image
        self.setGeometry(position[0], position[1], width, height)
        self.setStyleSheet(f"QPushButton {{ border-image: url({image}); }}")
        self.clicked.connect(self.on_clicked_wrapper if on_clicked else lambda: None)
        self.on_clicked = on_clicked  # Store the on_clicked function if provided


    def on_clicked_wrapper(self):
        if self.on_clicked:
            self.on_clicked()


#f = Fingerprint("/dev/ttyUSB0", 115200)
class NewUserWindow(QMainWindow):
    def __init__(self, column_list=None):
        super().__init__()
        #self.rfid_reader = SimpleMFRC522()
        #self.fingerprint = Fingerprint('/dev/ttyUSB1', 115200)

        # Check if column_list is None and provide a default empty list
        if column_list is None:
            column_list = []

        # Set window dimensions
        #self.rfid_reader = None
        #self.fingerprint.init()
        #self.fingerprint_thread = None
        self.width = 480
        self.height = 800
        self.setGeometry(0, 0, self.width, self.height)

        # Set background image
        self.background_image = QLabel(self)
        self.background_image.setPixmap(QPixmap("images/background.png"))
        self.background_image.setGeometry(0, 0, self.width, self.height)

        self.backbtn = imgbutton2(self, "images/icons/BackIcon.png", 30, 30, (5, 44), self.openUserMenu)
        self.backbtn.clicked.connect(self.close)

        # Create a QCalendarWidget
        self.calendar = QCalendarWidget(self)
        self.calendar.setWindowTitle("Select Date of Birth")
        self.calendar.setWindowFlags(Qt.Popup)
        #self.calendar.selectionChanged.connect(self.update_dob_from_calendar)
        self.calendar.hide()  # Initially, hide the calendar

        self.combo = QComboBox(self)  # Define self.combo here
        self.combo.addItems(column_list)
        self.combo.setEditable(True)
        self.combo.setInsertPolicy(QComboBox.NoInsert)
        self.combo.completer().setCompletionMode(QtWidgets.QCompleter.PopupCompletion)

        self.combo.setStyleSheet("QComboBox { height: 35px; }")
        self.combo.move(108, 96)
        self.combo.setFixedWidth(255)
        self.combo.setFixedHeight(30)

        #self.combo.activated.connect(self.open_virtual_keyboard)


        def get_employee_info(employee_id):
            with open('data/EmpMaster-Epitage.csv', 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) > 0 and row[0] == employee_id:
                        if len(row) > 2:
                            return row[1], row[2]  # Return EmployeeName and Date of Birth
                        else:
                            break  # Handle the case where the row doesn't have enough elements
            return None  # Return None if employee info is not found

        # Parse column from CSV file
        column_list = []
        dob_dict = {}  # Dictionary to store EmployeeName and Date of Birth mapping
        with open('data/EmpMaster-Epitage.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the first row if it contains headers
            for row in reader:
                if len(row) > 0:  # Check if the row has at least one element
                    column_list.append(row[0])  # Append EmpID to column_list
                    dob_dict[row[0]] = row[2]  # Store empID and Date of Birth mapping

        name_id = QLabel('ID:', self)
        name_id.move(18, 102)

        # Placeholder image path
        placeholder_image_path = "images/placeholderimg.png"

        # QLabel to display employee picture
        picture_label = QLabel(self)
        picture_label.setGeometry(369, 96, 94, 142)
        # picture_label.setStylesheet()
        picture_label.setPixmap(QPixmap(placeholder_image_path))
        picture_label.setScaledContents(True)

        combo = QComboBox(self)
        combo.addItems(column_list)
        combo.setEditable(True)
        combo.setInsertPolicy(QComboBox.NoInsert)
        combo.completer().setCompletionMode(QtWidgets.QCompleter.PopupCompletion)
        self.combo.installEventFilter(self)

        combo.setStyleSheet("QComboBox { height: 35px; }")
        combo.move(108, 96)
        combo.setFixedWidth(255)
        combo.setFixedHeight(30)
        combo.installEventFilter(self)

        def combo_text_changed():
            selected_employee_id = combo.currentText()
            if selected_employee_id:
                employee_info = get_employee_info(selected_employee_id)
                if employee_info is not None:
                    employee_name, dob = employee_info
                    self.text_id.setText(str(employee_name))  # Display EmployeeName
                    self.text_dob.setText(dob)
                    # Update employee picture based on the selected ID
                    image_path = f'data/emp-photos/{selected_employee_id}.jpg'  # Replace with your image path
                    picture_label.setPixmap(QPixmap(image_path))
                    return
            self.text_id.clear()
            self.text_dob.clear()
            picture_label.setPixmap(QPixmap(placeholder_image_path))  # Show placeholder image if no ID selected

        #combo.currentTextChanged.connect(combo_text_changed)
        # Connect the combo box clicked signal to the virtual keyboard function
        #self.combo.activated.connect(self.open_virtual_keyboard)


        def save_employee_info():
            employee_id = combo.currentText()
            employee_name = self.text_id.text()
            dob = self.text_dob.text()
            rfid = self.label_rfid.text()
            finger = self.label_fing.text()

            # Check if any of the fields are empty
            if not employee_id or not employee_name or not dob or not rfid or not finger:
                return

            # Open the CSV file in append mode and write the new user data
            with open('data/EmpMaster-Epitage.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([employee_id, employee_name, dob, rfid, finger])

            # Clear the input fields and reset the combo box
            combo.setCurrentIndex(-1)
            self.text_id.clear()
            self.text_dob.clear()
            self.label_rfid.clear()
            self.label_fing.clear()
            picture_label.setPixmap(QPixmap(placeholder_image_path))

            # Optional: Update the combo box and dob_dict with the new user data
            column_list.append(employee_id)
            dob_dict[employee_id] = dob
            combo.addItem(employee_id)

        save_button = QPushButton('Save', self)
        save_button.move(246, 729)
        save_button.setFixedSize(85, 35)
        save_button.clicked.connect(save_employee_info)


        name_id = QLabel('ID:', self)
        name_id.move(18, 102)

        # Placeholder image path
        placeholder_image_path = "images/placeholderimg.png"

        # QLabel to display employee picture
        picture_label = QLabel(self)
        picture_label.setGeometry(369, 96, 94, 142)
        # picture_label.setStylesheet()
        picture_label.setPixmap(QPixmap(placeholder_image_path))
        picture_label.setScaledContents(True)

        self.combo = QComboBox(self)
        self.combo.addItems(column_list)
        self.combo.setEditable(True)
        self.combo.setInsertPolicy(QComboBox.NoInsert)
        self.combo.completer().setCompletionMode(QtWidgets.QCompleter.PopupCompletion)

        self.combo.setStyleSheet("QComboBox { height: 35px; }")
        self.combo.move(108, 96)
        self.combo.setFixedWidth(255)
        self.combo.setFixedHeight(30)
        self.combo.installEventFilter(self)  # Install event filter for the combo box



        def combo_text_changed():
            selected_employee_id = self.combo.currentText()
            if selected_employee_id:
                employee_info = get_employee_info(selected_employee_id)
                if employee_info is not None:
                    employee_name, dob = employee_info
                    self.text_id.setText(str(employee_name))  # Display EmployeeName
                    self.text_dob.setText(dob)
                    # Update employee picture based on the selected ID
                    image_path = f'data/emp-photos/{selected_employee_id}.jpg'  # Replace with your image path
                    picture_label.setPixmap(QPixmap(image_path))
                    return
            self.text_id.clear()
            self.text_dob.clear()
            picture_label.setPixmap(QPixmap(placeholder_image_path))  # Show placeholder image if no ID selected
            self.text_dob.installEventFilter(self)

        #combo.currentTextChanged.connect(combo_text_changed)
        combo.installEventFilter(self)

        label_id = QLabel('Name', self)
        label_id.move(18, 139)

        self.text_id = QLineEdit(self)
        self.text_id.setReadOnly(False)
        self.text_id.move(108, 134)
        self.text_id.resize(255, 30)
        self.text_id.installEventFilter(self)

        label_photo = QLabel('Photo', self)
        label_photo.move(18, 176)

        text_photo = QLineEdit(self)
        text_photo.setReadOnly(False)
        text_photo.move(108, 171)
        text_photo.resize(255, 30)


        self.show()





    def openUserMenu(self):
        from UserMenu import UserWindow
        self.openUserMenu = UserWindow()
        self.openUserMenu.show()

    def scan_rfid(self):
        try:
            # Read data from the RFID card
            rfid_id = self.rfid_reader.read_id()
            self.label_rfid.setText(str(rfid_id))  # Display the RFID card ID in the corresponding box

        except Exception as e:
            print("Error scanning RFID card:", e)

    def capture_fingerprint(self):
        try:
            # Capture the fingerprint data from the sensor
            fingerprint = self.fingerprint.capture_finger(best=False)
            #captured = self.fingerprint.capture_finger(best=False)
            captured = self.fingerprint.enroll(fingerprint)
            idtemp = self.fingerprint.identify()
            self.label_fing.setText(str(idtemp))
            #fingerprint = f.capture_finger()
            #captured = f.enroll(fingerprint)
            # Return True if fingerprint captured successfully, False otherwise
            return captured

        except Exception as e:
            print("Error capturing fingerprint:", e)
            return False

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NewUserWindow()
    window.show()
    sys.exit(app.exec_())