from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel, QCalendarWidget, QFileDialog, QLineEdit, QMessageBox, QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QHeaderView
from PyQt5.QtCore import Qt, QEvent, QRect, QSize, QDate, pyqtSignal, QTimer, QThread

from ethos_main_window import EthosMainWindow
from utilities.img_button import ImgButton
from utilities.popup_1 import AcceptDialog
from utilities.keyboard import *
from utilities.year_selector import YearSelector
from utilities.popup_example import MainWindow, PopupDialog


from infrastructure.database.entity.employee import Employee
from infrastructure.database.entity.finger_point_scan import FingerPointScan

from controllers.employee_controller import EmployeeController
from controllers.role_controller import RoleController
from firmware.led import LEDStripController
# from firmware.write_rfid import RFIDWrite

import RPi.GPIO as GPIO
import datetime
import os
import shutil
import time
import pygame as pg

class EmployeeForm(EthosMainWindow):
    def __init__(self):
        super().__init__()
        self.led_controller = LEDStripController()  # Initialize the LED controller
        self.employeeController = EmployeeController()
        self.popup_dialogue = MainWindow()
        self.virtual_keyboard = VirtualKeyboard()

        self.enrolled_fingers = []  # Store enrolled finger IDs
        self.finger_buttons = {
            'LL': ImgButton(self, "LL.png", 55, 30, 55, 30, "#D9D9D9", 131, 420, self.handle_finger_button_click),
            'LR': ImgButton(self, "LR.png", 55, 30, 55, 30, "#D9D9D9", 201, 421, self.handle_finger_button_click),
            'LM': ImgButton(self, "LM.png", 55, 30, 55, 30, "#D9D9D9", 271, 421, self.handle_finger_button_click),
            'LI': ImgButton(self, "LI.png", 55, 30, 55, 30, "#D9D9D9", 341, 421, self.handle_finger_button_click),
            'LT': ImgButton(self, "LT.png", 55, 30, 55, 30, "#D9D9D9", 411, 421, self.handle_finger_button_click),
            'RL': ImgButton(self, "RL.png", 55, 30, 55, 30, "#D9D9D9", 131, 490, self.handle_finger_button_click),
            'RR': ImgButton(self, "RR.png", 55, 30, 55, 30, "#D9D9D9", 201, 490, self.handle_finger_button_click),
            'RM': ImgButton(self, "RM.png", 55, 30, 55, 30, "#D9D9D9", 271, 490, self.handle_finger_button_click),
            'RI': ImgButton(self, "RI.png", 55, 30, 55, 30, "#D9D9D9", 341, 490, self.handle_finger_button_click),
            'RT': ImgButton(self, "RT.png", 55, 30, 55, 30, "#D9D9D9", 411, 490, self.handle_finger_button_click),
        }
        # Dictionary to store enrolled finger IDs with their names
        self.enrolled_fingers_dict = {}
        # Adding buttons to the layout
        main_layout = QVBoxLayout()

        # First row layout
        row1_layout = QHBoxLayout()
        for button in list(self.finger_buttons.values())[:5]:
            row1_layout.addWidget(button)

        # Second row layout
        row2_layout = QHBoxLayout()
        for button in list(self.finger_buttons.values())[5:]:
            row2_layout.addWidget(button)

        main_layout.addLayout(row1_layout)
        main_layout.addLayout(row2_layout)

        button_widget = QWidget(self)
        button_widget.setLayout(main_layout)
        button_widget.setGeometry(115, 433, 373, 100)

        # Connect the clicked signal of each finger button to a slot
        for button in self.finger_buttons.values():
            button.clicked.connect(self.handle_finger_button_clicked)

        # Create a year selector widget
        self.year_selector = YearSelector(1945, 2050)
        self.year_selector.year_selected.connect(self.updateYearInCalendar)

        font = QFont("Inika", 12)

        self.ok_btn = ImgButton(
            self, "OK_btn.png", 85, 35, 85, 35, "#D9D9D9", 248, 729, self.save_employee_info)
        self.cancel_btn = ImgButton(
            self, "Cancel_btn.png", 85, 35, 85, 35, "#D9D9D9", 147, 729, self.cancel_button)

        self.name_id = QLabel('ID :', self)
        self.name_id.setFont(font)
        self.name_id.move(18, 102)
        self.newID = QLineEdit(self)
        self.newID.setReadOnly(False)
        self.newID.move(128, 96)
        self.newID.resize(335, 30)
        self.newID.setMaxLength(10)
        self.newID.installEventFilter(self)
        # self.textChanged.connect(self.handle_client_emp_id)
        self.newID.textChanged.connect(self.handle_client_emp_id)

        self.label_id = QLabel('Name :', self)
        self.label_id.setFont(font)
        self.label_id.move(18, 139)

        self.text_id = QLineEdit(self)
        self.text_id.setReadOnly(False)
        self.text_id.move(128, 134)
        self.text_id.resize(335, 30)
        self.text_id.setMaxLength(10)
        self.text_id.installEventFilter(self)

        self.label_photo = QLabel('Photo :', self)
        self.label_photo.setFont(font)
        self.label_photo.move(18, 176)
        self.text_photo = QLineEdit(self)
        self.text_photo.setReadOnly(False)
        self.text_photo.move(128, 171)
        self.text_photo.resize(335, 30)
        self.text_photo.installEventFilter(self)
        # self.text_photo.mousePressEvent = self.open_file_dialog
        self.magnifyingbtn = ImgButton(self, "MagnifyingGlass.png", 25,25,25,25,"#D9D9D9",435,174,self.open_file_dialog)

        self.calendar_widget = QCalendarWidget(self)
        self.calendar_widget.setGeometry(130, 240, 300, 300)
        headers = self.calendar_widget.findChildren(QHeaderView)
        for header in headers:
            header.setStyleSheet("background-color: orange; color: white;")


        self.calendar_widget.hide()
        self.label_dob = QLabel('Birth Date :', self)
        self.label_dob.setFont(font)
        self.label_dob.move(18, 213)
        self.text_dob = QLineEdit(self)
        self.text_dob.setReadOnly(False)
        self.text_dob.move(128, 208)
        self.text_dob.resize(335, 30)
        self.text_dob.installEventFilter(self)
        # self.text_dob.mousePressEvent = self.show_calendar
        self.calendar_widget.clicked.connect(self.handle_date_selection)
        self.calendar = ImgButton(self, "Calendar.png", 25,25,25,25,"#D9D9D9",435,211,self.show_calendar)


        #
        self.label_role = QLabel('Role  :', self)
        self.label_role.setFont(font)
        self.label_role.move(20, 255)
        self.role_dropdown = QComboBox(self)
        self.role_dropdown.move(128, 250)
        self.role_dropdown.setFixedSize(335, 30)
        self.role_dropdown.setEditable(True)
        self.role_dropdown.setCurrentIndex(0)
        self.role_dropdown.addItem("") 
        self.populateCombobox()
        # self.role_dropdown.installEventFilter(self)
        # Connect the currentIndexChanged signal to handle_role_selection slot
        self.role_dropdown.currentIndexChanged.connect(self.handle_role_selection)
        # self.role_dropdown.setStyleSheet("border: 2px solid orange;")

        self.label_rfid = QLineEdit(self)
        self.label_rfid.setReadOnly(False)
        self.label_rfid.setPlaceholderText(
            "Click in the box to Register your Card.")
        # self.label_rfid.mousePressEvent = self.write_rfid
        self.label_rfid.installEventFilter(self)
        # self.label_rfid.mousePressEvent = lambda event: self.write_rfid(event)
        self.label_rfid.move(131, 300)
        self.label_rfid.resize(335, 30)

        self.rfidcardbtn = ImgButton(
            self, "Card.png", 100, 100, 100, 100, "#D9D9D9", 20, 300, self.clear)

        self.label_fing = QLineEdit(self)
        self.label_fing.setReadOnly(False)
        self.label_fing.setPlaceholderText("Place your finger on the Reader")
        self.label_fing.move(132, 412)
        self.label_fing.resize(335, 30)
        self.fingerbtn = ImgButton(self, "FingerVeri_Icon.png", 100, 100, 100,
                                   100, "#D9D9D9", 20, 420, self.clear)

        self.label_face = QLineEdit(self)
        self.label_face.setReadOnly(False)
        self.label_face.move(131, 541)
        self.label_face.resize(335, 177)

        self.facebtn = ImgButton(self, "face.png",
                                 100, 100, 100, 100, "#D9D9D9", 20, 541, self.show_popup)
        self.facebtn.clicked.connect(self.show_popup)
        self.show()


        # self.text_id.setStyleSheet(
        #     """
        #     QLineEdit {
        #         /* Original QLineEdit style */
        #     }
        #     QLineEdit:focus {
        #         border: 2px solid orange; /* Change the border color when focused */
        #     }
        #     """
        # )

        # self.newID.setStyleSheet(
        #     """
        #     QLineEdit {
        #         /* Original QLineEdit style */
        #     }
        #     QLineEdit:focus {
        #         border: 2px solid orange; /* Change the border color when focused */
        #     }
        #     """
        # )
        # self.text_photo.setStyleSheet(
        #     """
        #     QLineEdit {
        #         /* Original QLineEdit style */
        #     }
        #     QLineEdit:focus {
        #         border: 2px solid orange; /* Change the border color when focused */
        #     }
        #     """
        # )
        # self.text_dob.setStyleSheet(
        #     """
        #     QLineEdit {
        #         /* Original QLineEdit style */
        #     }
        #     QLineEdit:focus {
        #         border: 2px solid orange; /* Change the border color when focused */
        #     }
        #     """
        # )
        # self.label_rfid.setStyleSheet(
        #     """
        #     QLineEdit {
        #         /* Original QLineEdit style */
        #     }
        #     QLineEdit:focus {
        #         border: 2px solid orange; /* Change the border color when focused */
        #     }
        #     """
        # )  
        self.show()
    
    def open_file_dialog(self, event=None):
        # Code to copy the selected image to the emp-photos folder.
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Photo", "", "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)", options=options)
        if file_path:
            # If a file is selected, set the file path to QLineEdit or do further processing
            self.text_photo.setText(file_path)
        
    def populateCombobox(self):
        self.role_dropdown.clear()
        # Create an instance of RoleController
        role_controller = RoleController()
        # Fetch all roles from RoleController
        roles = role_controller.get_all_roles()
        # Add fetched role names to the ComboBox
        for role in roles:
            # self.role_dropdown.addItem(role.role_id, role.role_name)
            self.role_dropdown.addItem(role.role_name)
            # Set role ID as item data
            self.role_dropdown.setItemData(self.role_dropdown.count() - 1, role.role_id)

    def handle_role_selection(self, index):
        selected_role = self.role_dropdown.itemData(index)
        print("Selected Role:", selected_role)
    
    def handle_client_emp_id(self, text):
        print("Checking if ID exists for:", text)
        is_id_exist = self.employeeController.verify_employee_client_emp_id(text)
        if is_id_exist:
            print("ID already exists")
            if self.newID.text() == text:
                # Clear the field only if the ID matches the current text
                self.newID.clear()
            # Check if the QMessageBox is already open for this ID
            if text not in getattr(self, 'shown_id_warnings', []):
                # Add the ID to the list of shown warnings
                self.shown_id_warnings = getattr(self, 'shown_id_warnings', []) + [text]
                id_warning_messagebox = QMessageBox(self)
                id_warning_messagebox.setWindowTitle("Duplicate Registration")
                id_warning_messagebox.setText("ID already exists.")
                id_warning_messagebox.show()
        else:
            print("ID does not exist")

    def cancel_button(self):
        self.newID.clear()
        self.text_id.clear()
        self.text_dob.clear()
        # self.label_photo.clear()
        self.text_photo.clear()
        self.label_rfid.clear()
        # self.label_fing.clear()
        # Clear the enrolled fingerprints list
        self.enrolled_fingers = []
        # After saving employee info successfully, reset button styles
        self.reset_button_styles()

        # Delete registered fingerprints from the sensor hardware
        self.delete_registered_fingerprints()
        self.role_dropdown.clear()
        self.role_dropdown.setCurrentIndex(-1)

    def delete_registered_fingerprints(self):
        """
        Delete registered fingerprints stored in the sensor hardware.
        """
        # Get the list of enrolled finger IDs
        enrolled_finger_ids = list(self.enrolled_fingers_dict.values())

        # Check if there are any enrolled finger IDs
        if enrolled_finger_ids:
            # Convert IDs to integers if necessary
            enrolled_finger_ids = [int(id) for id in enrolled_finger_ids]

            # Call the method to delete fingerprints
            self.delete_fingerprints(enrolled_finger_ids)
        else:
            print("No enrolled fingerprints to delete.")

    # ********    MOVE TO FIRMWARE CODE   {
    def delete_fingerprints(self, ids_to_delete):
        """
        Deletes fingerprint IDs provided in the list.
        """
        from firmware.fps_main import Fingerprint

        # Initialize the fingerprint controller
        f = Fingerprint("/dev/ttyUSB0", 115200)

        try:
            if f.init():
                for fingerprint_id in ids_to_delete:
                    result = f.delete(fingerprint_id)
                    if result:
                        print(f"Deletion of ID {fingerprint_id} successful!")
                    else:
                        print(f"Deletion of ID {fingerprint_id} failed.")
        except Exception as e:
            print("Error deleting fingerprints:", e)
        finally:
            f.close_serial()
    # ********                             }

    def write_rfid(self, event):
        # Stop the RFID thread if it's running
        if hasattr(self, 'rfid_thread') and self.rfid_thread.isRunning():
            self.rfid_thread.quit()  # Terminate the thread
            self.rfid_thread.wait()  # Wait for the thread to finish

        # Start a new thread to handle RFID card scanning
        # self.rfid_write = RFIDWrite(self.text_id.text())
        # self.rfid_write.start_write_thread()
        # self.employeeController.write_rfid()
        # self.employeeController.rfid_write.rfid_scanned.connect(self.handle_rfid_scanned)
        self.rfid_thread = RFIDThread(
            self.text_id.text(), self.led_controller)  # Pass the LED controller
        self.rfid_thread.rfid_scanned.connect(self.handle_rfid_scanned)
        self.rfid_thread.start()

        # Show a popup indicating that the card is being scanned
        self.popup = AcceptDialog("Scanning RFID card...")
        self.popup.exec_()

    def handle_rfid_scanned(self, id):
        # Close the popup after scanning the RFID card
        # self.label_rfid.setText(str(id))
        # self.rfid_write.rfid_scanned.connect(str(id))
        is_verified = self.employeeController.verify_employee_rf_id(str(id))
        print("id verified in db")
        
        if not is_verified:
            self.label_rfid.setText(str(id))
            print("New ID accepted for DB operation")
            # return self.label_rfid.setText(str(id))
        else:
            print("ID already existing in DB")
            QMessageBox.warning(
                        self, "Duplicate Registration", "RFID already exists.")
            self.employeeController.cleanup()
        self.popup.accept()
        print("ID displayed at label_rfid:", id)

    def closeEvent(self, event):
        # Clean up LED resources before closing the application
        self.led_controller.clear_leds()
        event.accept()  # Accept the close event

    def handle_finger_button_click(self):
        finger_id = self.enroll_finger()
        if finger_id:
            is_fps_exist = self.employeeController.verify_employee_fps(finger_id)
            if is_fps_exist:
                print("fps already exist")
                # self.employeeController.restart_connection()
                QMessageBox.warning(
                        self, "Duplicate Registration", "Finger already registered.")
            else:
                print("fps not exist")
                button = self.sender()
                finger_name = [
                    name for name, btn in self.finger_buttons.items() if btn == button][0]
                if finger_id in self.enrolled_fingers:
                    QMessageBox.warning(
                        self, "Duplicate Registration", "Finger already registered.")
                else:
                    self.enrolled_fingers.append(finger_id)
                    self.label_fing.setText(', '.join(self.enrolled_fingers))
                    self.update_button_appearance(button)
                    # Update the dictionary
                    self.enrolled_fingers_dict[finger_name] = finger_id

                    # Print the dictionary
                    self.print_enrolled_fingers_dict()

    def print_enrolled_fingers_dict(self):
        print("Enrolled Fingers Dictionary:")
        for finger_name, finger_id in self.enrolled_fingers_dict.items():
            print(f"Finger Name: {finger_name}, ID: {finger_id}")

    def update_button_appearance(self, button):
        button.setEnabled(False)
        button.setStyleSheet("color: gray;")

    def reset_button_styles(self):
        for button in self.finger_buttons.values():
            button.setEnabled(True)
            button.setStyleSheet("")  # Resetting the style sheet to default

    def handle_finger_button_clicked(self):
        # Get the sender button
        button = self.sender()

        # Apply the temporary style sheet to show the border
        button.setStyleSheet("border: 2px solid orange;")

        # Use a QTimer to remove the border after a short delay (e.g., 500 milliseconds)
        timer = QTimer(self)
        timer.timeout.connect(lambda: self.remove_border(button))
        timer.start(500)

        # Perform other actions if needed...

    def remove_border(self, button):
        # Remove the border after the delay
        button.setStyleSheet("")

    def save_employee_info(self):
         # Check if any compulsory field is blank
        if (not self.newID.text() or
            not self.text_id.text() or
            not self.text_dob.text() or
            not self.label_rfid.text() or
            not self.text_photo.text() or
            self.role_dropdown.currentIndex() == -1 or
            not self.enrolled_fingers_dict):
            
            # If any compulsory field is blank, show a warning message
            QMessageBox.warning(
                self, "Incomplete Information", "All fields are compulsory. Please fill in all fields.")
            return
        
        fps = FingerPointScan(
            None,
            None,
            self.enrolled_fingers_dict.get("LL"),
            self.enrolled_fingers_dict.get("LR"),
            self.enrolled_fingers_dict.get("LM"),
            self.enrolled_fingers_dict.get("LI"),
            self.enrolled_fingers_dict.get("LT"),
            self.enrolled_fingers_dict.get("RL"),
            self.enrolled_fingers_dict.get("RR"),
            self.enrolled_fingers_dict.get("RM"),
            self.enrolled_fingers_dict.get("RI"),
            self.enrolled_fingers_dict.get("RT"),
        )

        employee_row = Employee(
            None,
            self.newID.text(),
            self.text_id.text(),
            # self.label_rfid.setText(str(id)),
            self.text_dob.text(),
            self.label_rfid.text(),
            fps, 
            "", 
            "", 
            self.role_dropdown.currentData(), 
            self.text_photo.text(),
            )

        if not employee_row.client_emp_id or not employee_row.emp_name or not employee_row.emp_dob or not employee_row.rf_id:
            print("validation error")
            return

        print("saving to employee controller")
        self.employeeController.create_employee(employee_row)
        # Close DB Connection
        self.newID.clear()
        self.text_id.clear()
        self.text_dob.clear()
        self.label_rfid.clear()
        self.label_fing.clear()
        self.text_photo.clear()
        # Clear the enrolled fingerprints list
        self.enrolled_fingers = []
        # After saving employee info successfully, reset button styles
        self.reset_button_styles()
        self.role_dropdown.clear()
        self.populateCombobox()
        self.role_dropdown.setCurrentIndex(-1)
        self.enrolled_fingers_dict.clear()
        self.employeeController.restart_connection()

        QMessageBox.information(
        self, "Success", "Employee information saved successfully.")
        freq = 44100    # audio CD quality
        bitsize = -16   # unsigned 16 bit
        channels = 2    # 1 is mono, 2 is stereo
        buffer = 2048   # number of samples (experiment to get right sound)
        pg.mixer.init(freq, bitsize, channels, buffer)
        # optional volume 0 to 1.0
        pg.mixer.music.set_volume(1.0)
        # Load the MP3 file
        pg.mixer.music.load('thank-you-168416.mp3')
        # Play the audio file
        pg.mixer.music.play()

    def validate_age(self, dob_text):
        try:
            dob = datetime.datetime.strptime(dob_text, '%Y-%m-%d')
            today = datetime.datetime.today()
            age = today.year - dob.year - \
                ((today.month, today.day) < (dob.month, dob.day))
            if age >= 18:
                return True
            else:
                return False
        except ValueError:
            return False

    def navigate_back(self):
        from UserMenu import UserWindow
        self.virtual_keyboard.close()
        self.openUserMenu = UserWindow()
        self.openUserMenu.show()
        self.close()

    def eventFilter(self, obj, event):
        if event and hasattr(event, 'type'):
            if obj == self.text_dob and event is not None and event.type() == QEvent.Type.MouseButtonPress:
                self.show_calendar(event)
                # self.text_dob.mousePressEvent = self.show_calendar
                self.text_dob.setStyleSheet("border: 2px solid orange;")
                self.remove_border(self.text_photo)
                self.remove_border(self.newID)
                self.remove_border(self.text_id)
                self.remove_border(self.label_rfid)
                self.virtual_keyboard.close()
                return True
            elif obj == self.text_id and event is not None and event.type() == QEvent.Type.MouseButtonPress:
                self.open_virtual_keyboard(self.text_id)
                self.text_id.setStyleSheet("border: 2px solid orange;")
                self.remove_border(self.newID)
                self.remove_border(self.text_photo)
                self.remove_border(self.text_dob)
                self.remove_border(self.label_rfid)
                return True
            elif obj == self.newID and event is not None and event.type() == QEvent.Type.MouseButtonPress:
                self.open_virtual_keyboard(self.newID)
                self.newID.setStyleSheet("border: 2px solid orange;")
                self.remove_border(self.text_id)
                self.remove_border(self.text_photo)
                self.remove_border(self.text_dob)
                self.remove_border(self.label_rfid)
                return True
            elif obj == self.text_photo and event is not None and event.type() == QEvent.Type.MouseButtonPress:
                self.open_file_dialog(event)
                self.text_photo.setStyleSheet("border: 2px solid orange;")
                self.remove_border(self.text_id)
                self.remove_border(self.newID)
                self.remove_border(self.text_dob)
                self.remove_border(self.label_rfid)
                self.virtual_keyboard.close()
                return True
            # elif obj == self.role_dropdown and event is not None and event.type() == QEvent.Type.MouseButtonPress:
            #     self.role_dropdown.setStyleSheet("QComboBox: 2px solid orange;")
            #     # time.sleep(2)
            #     # self.remove_border(self.role_dropdown)
            #     self.remove_border(self.text_id)
            #     self.remove_border(self.newID)
            #     self.remove_border(self.text_dob)
            #     self.remove_border(self.text_photo)
            #     self.remove_border(self.label_rfid)
            #     self.virtual_keyboard.close()
            #     return True
            elif obj == self.label_rfid and event is not None and event.type() == QEvent.Type.MouseButtonPress:
                self.write_rfid(event)
                self.label_rfid.setStyleSheet("border: 2px solid orange;")
                self.remove_border(self.text_id)
                self.remove_border(self.newID)
                self.remove_border(self.text_dob)
                self.remove_border(self.text_photo)
                self.virtual_keyboard.close()
                return True
            elif event is not None and event.type() == QEvent.Type.MouseButtonPress:
                # self.text_photo.mousePressEvent = self.open_file_dialog
                # self.role_dropdown.currentIndexChanged.connect(self.handle_role_selection)
                # self.role_dropdown.setStyleSheet("border: 2px solid orange;")
                self.remove_border(self.label_rfid)
                self.remove_border(self.text_id)
                self.remove_border(self.newID)
                self.remove_border(self.text_dob)
                self.remove_border(self.text_photo)
                self.virtual_keyboard.close()
                return True
        return super().eventFilter(obj, event)


    def show_calendar(self, event=None):
        if event is not None:
            event.accept()

        self.year_selector.setGeometry(QRect(self.text_dob.mapToGlobal(
            self.text_dob.rect().bottomLeft()), QSize(150, 150)))
        self.year_selector.show()
        self.year_selector.raise_()
        self.calendar_widget.hide()
        self.year_selector.year_selected.connect(self.show_month_calendar)
    
    def show_month_calendar(self, year):
        self.calendar_widget.setSelectedDate(
            QDate(year, self.calendar_widget.selectedDate().month(), 1))
        bottom_left = self.text_dob.mapToGlobal(
            self.text_dob.rect().bottomLeft())
        self.calendar_widget.setGeometry(
            bottom_left.x(), bottom_left.y(), 300, 300)
        self.calendar_widget.show()
        self.calendar_widget.raise_()
        self.year_selector.year_selected.disconnect(self.show_month_calendar)

    def updateYearInCalendar(self, year):
        self.calendar_widget.setSelectedDate(
            QDate(year, self.calendar_widget.selectedDate().month(), 1))
        selected_date = self.calendar_widget.selectedDate()
        self.text_dob.setText(selected_date.toString(Qt.ISODate))
        self.year_selector.hide()
        bottom_left = self.text_dob.mapToGlobal(
            self.text_dob.rect().bottomLeft())
        self.calendar_widget.setGeometry(
            bottom_left.x(), bottom_left.y(), 300, 300)
        self.calendar_widget.show()
        self.calendar_widget.raise_()

    def handle_date_selection(self, date):
        self.text_dob.setText(date.toString(Qt.ISODate))
        self.calendar_widget.hide()
        dob_text = self.text_dob.text()
        if dob_text:
            if not self.validate_age(dob_text):
                self.text_dob.clear()
                QMessageBox.critical(self, "Age Requirement", "Age must be 18 years or above.")

    def open_virtual_keyboard(self, target):
        if hasattr(self, 'virtual_keyboard') and self.virtual_keyboard.isVisible():
            self.virtual_keyboard.close() 

        # self.virtual_keyboard = VirtualKeyboard()
        self.virtual_keyboard.target = target

        screen_geometry = QGuiApplication.primaryScreen().geometry()
        keyboard_x = 0
        keyboard_y = screen_geometry.height() - self.virtual_keyboard.height() + 280

        self.virtual_keyboard.move(keyboard_x, keyboard_y)
        self.virtual_keyboard.show()

        target.setAttribute(Qt.WA_InputMethodEnabled)

    def show_popup(self):
        popup = QMessageBox()
        popup.setText("Contact with Administrator")
        popup.setIcon(QMessageBox.Information)
        popup.setWindowTitle("Warning")
        popup.addButton(QMessageBox.Ok)
        popup.exec_()

    def enroll_finger(self):
        from firmware.fps_main import Fingerprint
        f = Fingerprint("/dev/ttyUSB0", 115200)
        count = f.get_enrolled_cnt()

        try:
            # while f.get_enrolled_cnt() != count + 1:
            # time.sleep(0.5)
            # idtemp = str(f.identify())
            if f.init():
                print("Enroll Fingerprint: %s" % str(f.enroll()))
                f.enroll()
                time.sleep(0.5)
                # count = count + 1
                idtemp = str(f.identify())
                return idtemp
            else:
                self.popup_dialogue = PopupDialog("Sorry, Finger Sensor Failed To Connect!")
                self.popup_dialogue.show()
                self.led_controller.set_orange()
                time.sleep(2)
                self.led_controller.clear_leds()
                self.popup_dialogue.accept()
        except Exception as e:
            print("Error capturing fingerprint:", e)
            f.close_serial()
            return False

    def clear(self):
        print("Click on Qlineedit to scan RFID card.")

# ********    MOVE TO FIRMWARE CODE   {

class RFIDThread(QThread):
    rfid_scanned = pyqtSignal(str)  # Define a signal to pass RFID data

    # Pass the LED controller as an argument
    def __init__(self, text, led_controller, parent=None):
        super().__init__(parent)
        self.text = text
        self.running = False
        self.led_controller = led_controller  # Initialize the LED controller

    def run(self):
        self.running = True
        try:
            # Perform RFID scanning operation here
            from mfrc522 import SimpleMFRC522
            reader = SimpleMFRC522()
            print("Now place your tag to write")
            self.led_controller.set_purple()  # Set LED to purple while scanning
            id, text = reader.write(self.text)
            print("Written")
            print("id", id)
            print("text", text)
            print(self.text)
            self.rfid_scanned.emit(str(id))  # Emit the scanned RFID data
        except Exception as e:
            print("Error capturing RFID:", e)
        finally:
            self.led_controller.clear_leds()  # Clear LEDs after RFID operation
            self.running = False

# # ********                             }

