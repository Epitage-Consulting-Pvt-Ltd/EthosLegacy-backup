from PyQt5.QtWidgets import QLabel, QLineEdit, QComboBox, QCompleter, QMessageBox, QCalendarWidget
from PyQt5.QtGui import QPixmap, QPixmap, QFont, QGuiApplication
from PyQt5.QtCore import QEvent
from ethos_main_window import EthosMainWindow
from NewUserV4 import *
from utilities.keyboard import VirtualKeyboard
from utilities.img_button import ImgButton
from utilities.year_selector import YearSelector
from infrastructure.database.entity.employee import Employee
from infrastructure.database.entity.finger_point_scan import FingerPointScan
from controllers.employee_controller import EmployeeController
from firmware.led import LEDStripController
from shutil import copyfile

class EditUserWindow(EthosMainWindow):
    def __init__(self):
        super().__init__()
        self.employeeController = EmployeeController()
        font = QFont("Inika", 12)
        # QLabel to display employee picture
        self.picture_label = QLabel(self)
        self.picture_label.setGeometry(369, 96, 94, 142)
        self.picture_label.setPixmap(
            QPixmap("placeholderImg.png"))
        self.picture_label.setScaledContents(True)
        # QComboBox for employee search
        name_id = QLabel('ID:', self)
        name_id.setFont(font)
        name_id.move(18, 102)
        self.combo = QComboBox(self)
        self.combo.setStyleSheet("QComboBox { height: 35px; }")
        self.combo.move(128, 96)
        self.combo.setFixedWidth(235)
        self.combo.setFixedHeight(30)
        self.combo.setEditable(True)
        self.combo.setInsertPolicy(QComboBox.NoInsert)
        self.completer = QCompleter()
        self.completer.setCompletionMode(QCompleter.PopupCompletion)
        self.combo.setCompleter(self.completer)
        # Attach a virtual keyboard to the combo box
        self.virtual_keyboard = VirtualKeyboard()
        self.virtual_keyboard.target = self.combo.lineEdit()  # Set the target QLineEdit
        # Connect textChanged signal of the combobox to combo_text_changed function
        self.combo.lineEdit().textChanged.connect(self.combo_text_changed)
        # Install event filter to open virtual keyboard on combo box click
        self.combo.installEventFilter(self)
        
        # Labels and LineEdits for displaying employee information
        self.label_id = QLabel('Name', self)
        self.label_id.setFont(font)
        self.label_id.move(18, 139)

        self.text_id = QLineEdit(self)
        self.text_id.setReadOnly(True)
        self.text_id.setDisabled(True)
        self.text_id.removeEventFilter(self)
        
        self.text_id.move(128, 134)
        self.text_id.resize(235, 30)
        self.text_id.setMaxLength(50)

        ###
        self.label_photo = QLabel('Photo', self)
        self.label_photo.setFont(font)
        self.label_photo.move(18, 176)

        self.text_photo = QLineEdit(self)
        self.text_photo.setReadOnly(True)
        self.text_photo.setDisabled(True)
        self.text_photo.removeEventFilter(self)

        self.text_photo.move(128, 171)
        self.text_photo.resize(235, 30)
        # self.text_photo.mousePressEvent = self.open_file_dialog
        self.magnifyingbtn = ImgButton(self, "MagnifyingGlass.png",
                                       25, 25, 25, 25, "#D9D9D9", 336, 174, self.open_file_dialog)
        self.magnifyingbtn.setDisabled(True)
        self.image_label = QLabel(self)
        self.image_label.setGeometry(369, 96, 97, 184)

        ###
        self.calendar_widget = QCalendarWidget(self)
        self.calendar_widget.setGeometry(130, 240, 300, 300)
        self.calendar_widget.setStyleSheet(
            "QCalendarWidget QHeaderView { background-color: #CCCCCC; }")
        self.calendar_widget.hide()
        self.label_dob = QLabel('Birth Date', self)
        self.label_dob.setFont(font)
        self.label_dob.move(18, 213)

        self.text_dob = QLineEdit(self)
        self.text_dob.setReadOnly(True)
        self.text_dob.setDisabled(True)
        self.text_dob.removeEventFilter(self)

        self.text_dob.move(128, 208)
        self.text_dob.resize(235, 30)
        # self.text_dob.mousePressEvent = self.show_calendar
        self.year_selector = YearSelector(1945, 2050)
        self.year_selector.year_selected.connect(self.updateYearInCalendar)
        self.calendar_widget.clicked.connect(self.handle_date_selection)
        # self.text_dob.editingFinished.connect(self.validate_age_on_date_editing_finished)
        self.calendar = ImgButton(self, "Calendar.png",
                                  25, 25, 25, 25, "#D9D9D9", 336, 211, self.show_calendar)
        self.calendar.setDisabled(True)

        ###
        self.label_role = QLabel('Role  :', self)
        self.label_role.setFont(font)
        self.label_role.move(20, 255)

        self.role_dropdown = QComboBox(self)
        self.role_dropdown.setEditable(False)
        self.role_dropdown.setDisabled(True)
        self.role_dropdown.removeEventFilter(self)

        self.role_dropdown.move(128, 250)
        self.role_dropdown.setFixedSize(235, 30)
        self.combo.setInsertPolicy(QComboBox.NoInsert)
        self.role_dropdown.addItem("")
        self.populateCombobox()

        ###
        self.led_controller = LEDStripController()  # Initialize the LED controller
        self.rfid = RFIDThread(self.text_id.text(), self.led_controller)
        self.rfid_rewrite = EmployeeForm()

        self.label_rfid = QLineEdit(self)
        self.label_rfid.setReadOnly(True)
        self.label_rfid.setDisabled(True)
        self.label_rfid.removeEventFilter(self)
        
        self.label_rfid.move(131, 300)
        self.label_rfid.resize(335, 30)
        self.rfidcardbtn = ImgButton(
            self, "Card.png", 100, 100, 100, 100, "#D9D9D9", 20, 300, self.clear)
        ###
        self.label_fing = QLineEdit(self)
        self.label_fing.setReadOnly(True)
        self.label_fing.setDisabled(True)
        self.label_fing.move(132, 412)
        self.label_fing.resize(335, 30)
        self.fingerbtn = ImgButton(self, "FingerVeri_Icon.png", 100, 100, 100,
                                   100, "#D9D9D9", 20, 420, self.clear)
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
        for self.button in self.finger_buttons.values():
            self.button.setDisabled(True)
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
        ###
        font = QFont("Inika", 12)
        self.ok_btn = ImgButton(
            self, "OK_btn.png", 85, 35, 85, 35, "#D9D9D9", 248, 729, self.save_employee_info)
        self.cancel_btn = ImgButton(
            self, "Cancel_btn.png", 85, 35, 85, 35, "#D9D9D9", 147, 729, self.cancel_button)
        # Open and show the window
        self.show()

    def eventFilter(self, obj, event):
        if event and hasattr(event, 'type'):
            if obj == self.combo and event.type() == QEvent.Type.MouseButtonPress:
                # Close the virtual keyboard associated with the combo box if it's open
                if hasattr(self, 'virtual_keyboard') and self.virtual_keyboard.isVisible():
                    self.virtual_keyboard.close()
                # Open a new virtual keyboard for the combo box
                self.open_virtual_keyboard(self.combo.lineEdit())
                return True
            elif obj == self.text_id and event is not None and event.type() == QEvent.Type.MouseButtonPress:
                self.open_virtual_keyboard(self.text_id)
            elif obj == self.label_rfid and event is not None and event.type() == QEvent.Type.MouseButtonPress:
                self.label_rfid.mousePressEvent = self.rfid.start()
                self.rfid.rfid_scanned.connect(self.update_rfid)
            elif obj == self.role_dropdown and event is not None and event.type() == QEvent.Type.MouseButtonPress:
                self.role_dropdown.currentIndexChanged.connect(self.handle_role_selection)
            elif obj == self.text_dob and event is not None and event.type() == QEvent.Type.MouseButtonPress:
                self.show_calendar(event)
            elif obj == self.text_photo and event is not None and event.type() == QEvent.Type.MouseButtonPress:
                self.open_file_dialog(event)
        return super().eventFilter(obj, event)

    def showVirtualKeyboard(self):
        screen_geometry = QGuiApplication.primaryScreen().geometry()
        keyboard_x = 0
        keyboard_y = screen_geometry.height() - self.virtual_keyboard.height() + 250

        self.virtual_keyboard.move(keyboard_x, keyboard_y)
        self.virtual_keyboard.show()

    def open_virtual_keyboard(self, target):
        if hasattr(self, 'virtual_keyboard') and self.virtual_keyboard.isVisible():
            self.virtual_keyboard.close()
        self.virtual_keyboard.target = target
        #
        screen_geometry = QGuiApplication.primaryScreen().geometry()
        keyboard_x = 0
        keyboard_y = screen_geometry.height() - self.virtual_keyboard.height() + 280
        #
        self.virtual_keyboard.move(keyboard_x, keyboard_y)
        self.virtual_keyboard.show()

    def combo_text_changed(self, text):
        results = self.employeeController.get_all_employees_by_search_text(
            text)
        #
        if results:
            # Assuming we take the first result if there are multiple matches
            employee = results[0]
            self.emp_id = employee.emp_id
            emp_name = employee.emp_name
            emp_dob = employee.emp_dob
            rf_id = employee.rf_id
            role_id = employee.role_id
            emp_photo = employee.emp_image
            self.text_id.setText(emp_name)
            self.text_dob.setText(emp_dob)
            self.label_rfid.setText(str(rf_id))
            self.text_photo.setText(emp_photo)
            pixmap = QPixmap(emp_photo)
            self.image_label.setPixmap(pixmap)
            self.image_label.setScaledContents(True)
            for role in self.roles:
                if role_id == role.role_id:
                    self.role_dropdown.setCurrentText(role.role_name)
                    pass

            self.text_id.setEnabled(True)
            self.text_id.setReadOnly(False)
            self.text_id.installEventFilter(self)
            
            self.text_dob.setEnabled(True)
            self.text_dob.setReadOnly(False)
            self.text_dob.installEventFilter(self)
            self.calendar.setEnabled(True)

            self.text_photo.setEnabled(True)
            self.text_photo.setReadOnly(False)
            self.text_photo.installEventFilter(self)
            self.magnifyingbtn.setEnabled(True)

            self.role_dropdown.setEnabled(True)

            self.label_rfid.setEnabled(True)
            self.label_rfid.setReadOnly(False)
            self.label_rfid.setDisabled(False)
            self.label_rfid.installEventFilter(self)

            self.label_fing.setEnabled(True)
            self.label_fing.setReadOnly(False)
            for self.button in self.finger_buttons.values():
                self.button.setDisabled(False)

        else:
            # Clear the fields if no employee is found
            self.text_id.clear()
            self.text_id.setReadOnly(True)
            self.text_id.setDisabled(True)
            self.text_id.removeEventFilter(self)

            self.text_dob.clear()
            self.text_dob.setReadOnly(True)
            self.text_dob.setDisabled(True)
            self.text_dob.removeEventFilter(self)

            self.text_photo.clear()
            self.text_photo.setReadOnly(True)
            self.text_photo.setDisabled(True)
            self.text_photo.removeEventFilter(self)
            self.image_label.clear()

            self.role_dropdown.setDisabled(True)

            self.label_rfid.clear()
            self.label_rfid.setReadOnly(True)
            self.label_rfid.setDisabled(True)
            self.label_rfid.removeEventFilter(self)

            self.label_fing.clear()
            self.label_fing.setDisabled(True)
            self.label_fing.setReadOnly(True)
            for self.button in self.finger_buttons.values():
                self.button.setDisabled(True)

    def populateCombobox(self):
        self.role_dropdown.clear()
        self.role_dropdown.setCurrentIndex(-1)
        # Create an instance of RoleController
        role_controller = RoleController()
        # Fetch all roles from RoleController
        self.roles = role_controller.get_all_roles()
        # Add fetched role names to the ComboBox
        for role in self.roles:
            self.role_dropdown.addItem(role.role_name)
            # Set role ID as item data
            self.role_dropdown.setItemData(
                self.role_dropdown.count() - 1, role.role_id)

    def handle_role_selection(self, index):
        selected_role = self.role_dropdown.itemData(index)

        print("Selected Role:", selected_role)

    def open_file_dialog(self, event=None):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Photo", "", "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)", options=options)
        if file_path:
            # If a file is selected, set the file path to QLineEdit or do further processing
            self.text_photo.setText(file_path)

    def show_calendar(self, event=None):
        if event:
            event.accept()

        self.year_selector.setGeometry(QRect(self.text_dob.mapToGlobal(
            self.text_dob.rect().bottomLeft()), QSize(150, 150)))
        self.year_selector.show()
        self.year_selector.raise_()
        self.calendar_widget.hide()
        # event.accept()
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

    def validate_age_on_date_editing_finished(self):
        dob_text = self.text_dob.text()
        if not self.validate_age(dob_text):
            QMessageBox.critical(self, "Age Requirement",
                                 "Age must be 18 years or above.")

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

    def update_rfid(self, id):
        print("rfid received:", id)
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
        # self.popup.accept()
        print("ID displayed at label_rfid:", id)

    def handle_finger_button_clicked(self):
        # Get the sender button
        button = self.sender()

        # Apply the temporary style sheet to show the border
        button.setStyleSheet("border: 2px solid orange;")

        # Use a QTimer to remove the border after a short delay (e.g., 500 milliseconds)
        timer = QTimer(self)
        timer.timeout.connect(lambda: self.remove_border(button))
        timer.start(500)

    def remove_border(self, button):
        # Remove the border after the delay
        button.setStyleSheet("")

    def enroll_finger(self):
        from firmware.fps_main import Fingerprint
        f = Fingerprint("/dev/ttyUSB0", 115200)

        try:
            if f.init():
                print("Enroll Fingerprint: %s" % str(f.enroll()))
                f.enroll()
                idtemp = str(f.identify())
                return idtemp
        except Exception as e:
            print("Error capturing fingerprint:", e)
            f.close_serial()
            return False

    def handle_finger_button_click(self):
        finger_id = self.enroll_finger()
        if finger_id:
            is_fps_exist = self.employeeController.verify_employee_fps(
                finger_id)
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

    def update_button_appearance(self, button):
        button.setEnabled(False)
        button.setStyleSheet("color: gray;")

    def reset_button_styles(self):
        for button in self.finger_buttons.values():
            button.setEnabled(True)
            button.setStyleSheet("")  # Resetting the style sheet to default

    def navigate_back(self):
        from UserMenu import UserWindow
        self.virtual_keyboard.close()
        self.openUserMenu = UserWindow()
        self.openUserMenu.show()
        self.close()

    def save_employee_info(self):
        # Check if any compulsory field is blank
        if (not self.text_id.text() or
            not self.text_dob.text() or
            not self.label_rfid.text() or
            not self.text_photo.text() or
            self.role_dropdown.currentIndex() == -1): #or
            #not self.enrolled_fingers_dict):
            
            # If any compulsory field is blank, show a warning message
            QMessageBox.warning(
                self, "Incomplete Information", "All fields are compulsory. Please fill in all fields.")
            return
        fps = FingerPointScan(None, None, None, None, None,
                              None, None, None, None, None, None, None,)

        employee_row = Employee(
            None,               # Placeholder for emp_id, assuming it's auto-generated
            self.combo.currentText(),
            self.text_id.text(),
            self.text_dob.text(),
            self.label_rfid.text(),
            fps,
            "",                 # Placeholder for face_id, assuming it's empty initially
            "",                 # Placeholder for mesh_id, assuming it's empty initially
            # Placeholder for role_id, assuming it's empty initially
            self.role_dropdown.currentData(),
            # Placeholder for emp_image, assuming it's empty initially
            self.text_photo.text(),
        )

        if not employee_row.client_emp_id or not employee_row.emp_name or not employee_row.emp_dob \
            or not employee_row.rf_id or not employee_row.emp_image:
            print("validation error")
            return

        print("Saving employee information...")
        self.employeeController.update_employee(self.emp_id, employee_row)

        self.combo.clearEditText()
        self.text_id.clear()
        self.text_dob.clear()
        self.label_rfid.clear()
        self.label_fing.clear()
        self.text_photo.clear()
        self.image_label.clear()
        self.image_label.clear()
        # Clear the enrolled fingerprints list
        self.enrolled_fingers = []
        self.role_dropdown.clear()
        self.populateCombobox()
        self.role_dropdown.setCurrentIndex(-1)
        # self.combo.clear()

        QMessageBox.information(
        self, "Success", "Employee information saved successfully.")

    def cancel_button(self):
        self.combo.clearEditText()
        self.text_id.clear()
        self.text_dob.clear()
        self.label_rfid.clear()
        self.label_fing.clear()
        self.text_photo.clear()
        self.image_label.clear()
        # Clear the enrolled fingerprints list
        self.enrolled_fingers = []
        self.role_dropdown.clear()
        self.populateCombobox()
        self.role_dropdown.setCurrentIndex(-1)
        self.text_id.clear()
        self.text_photo.clear()
        self.text_dob.clear()
        self.label_rfid.clear()
        self.label_fing.clear()
        self.text_photo.clear()
        self.image_label.clear()
        self.text_id.setDisabled(True)
        self.text_dob.setDisabled(True)
        self.text_photo.setDisabled(True)
        self.label_rfid.setDisabled(True)
        self.label_fing.setDisabled(True)
        self.role_dropdown.setDisabled(True)
        self.text_id.setReadOnly(True)
        self.text_photo.setReadOnly(True)
        self.text_dob.setReadOnly(True)
        self.label_rfid.setReadOnly(True)
        self.label_fing.setReadOnly(True)
        self.text_id.removeEventFilter(self)
        self.text_dob.removeEventFilter(self)
        self.label_rfid.removeEventFilter(self)

    def clear(self):
        print("Click on Qlineedit to scan RFID card.")