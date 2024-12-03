from firmware.rfid_read import RFIDReader
from infrastructure.database.repository.employee_repository import EmployeeRepository
from infrastructure.database.entity.employee import Employee
from firmware.led import LEDStripController
# from firmware.fps_verify import VerifyFingerprint
# from firmware.rfid_read import *
from firmware.read_rfid1 import *
from firmware.write_rfid import RFIDWrite


class EmployeeController:
    def __init__(self):
        self.rfid_reader = RFIDReader()
        # self.rfid_write = RFIDWrite()
        self.set_led = LEDStripController()

        # self.fingerprint_verifier = VerifyFingerprint()
        self.employee_repository = EmployeeRepository()
        self.verify_user = Signal_manager()
        self.verify_user.rfid_id.connect(lambda rf_id: self.verify(rf_id))
    
    def get_employee_by_id(self, client_emp_id):
        return self.employee_repository.get_employee_by_id(client_emp_id)

    def create_employee(self, employee):
        try:
            # validation
            self.employee_repository.create_employee(employee)
            print("employee saved successfully:", employee)
        except Exception as e:
            print("employee save failed:", e)

    def update_employee(self, emp_id, updated_employee):
        try:
            self.employee_repository.update_employee(emp_id, updated_employee)
            print("employee info updated")
        except Exception as e:
            print("Update employee Failed! :", e)

    def delete_employee_rfid_fps_face_photo(self, emp_id, is_rfid, is_fps, is_face, is_photo):
        self.employee_repository.delete_employee_rfid_fps_face_photo(
            emp_id, is_rfid, is_fps, is_face, is_photo)

    def verify_employee_client_emp_id(self, client_emp_id):
        return self.employee_repository.verify_employee_client_emp_id(client_emp_id)

    def verify_employee_rf_id(self, rf_id):
        return self.employee_repository.verify_employee_rf_id(rf_id)

    def verify_employee_fps(self, fps):
        return self.employee_repository.verify_employee_fps(fps)

    def get_all_employees_by_search_text(self, searchText):
        return self.employee_repository.get_all_employees_by_search_text(searchText)
    
    def get_employee_by_id(self, searchText):
        return self.employee_repository.get_employee_by_id(searchText)

    def restart_connection(self):
        self.employee_repository.close_connection()
        sleep(0.1)
        self.employee_repository.start_connection()

    def read_rfid(self):
        print("Reading RFID...")
        self.rfid_reader.start_reading_thread()

    # def write_rfid(self):
    #     print("Writing to rfid..")
    #     self.rfid_write.start_write_thread()
        # return self.rfid_write.rfid_scanned()

    # def verify_fingerprint(self):
    #     print("Verifying Fingerprint...")
    #     self.fingerprint_verifier.start_fps_thread()

    # def verify_user(self, rf_id):
    #     rfid = rf_id
    #     user=self.employee_repository.verify_user(rfid)
    #     if not user is None:
    #         self.set_led.set_green()
    #     else:
    #         self.set_led.set_red()

    def cleanup(self):
        print("Cleaning up RFID...")
        self.rfid_reader.cleanup_rfid()
        self.rfid_reader.wait_for_read_thread()
        # self.rfid_write.cleanup_rfid()
        # self.rfid_write.wait_for_write_thread()
        # self.fingerprint_verifier.cleanup_fps()
        # self.fingerprint_verifier.wait_for_fps_thread()
