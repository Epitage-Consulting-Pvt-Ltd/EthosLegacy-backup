from infrastructure.database.db_manager import DBManager
from infrastructure.database.entity.employee import Employee
from infrastructure.database.entity.finger_point_scan import FingerPointScan
from time import sleep


class EmployeeRepository:
    def __init__(self):
        self.db_manager = DBManager()

    def verify_user(self, rf_id):
        query = "SELECT * FROM employee WHERE rf_id=?"
        params = (rf_id,)
        result = self.db_manager.fetch_data(query, params)
        if result:
            print("employee verified")
            return self._create_employee_instance(result[0])
        return None

    def create_employee(self, employee):
        try:
            # Begin transaction
            self.db_manager.begin_transaction()

            query = """
                INSERT INTO employee (client_emp_id, emp_name, emp_dob, rf_id, face_id, mesh_id, role_id, emp_image)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """
            params = (employee.client_emp_id, employee.emp_name, employee.emp_dob, employee.rf_id,
                    employee.face_id, employee.mesh_id, employee.role_id, employee.emp_image)
            self.db_manager.execute_query_without_commit(query, params)

            # Retrieve the last inserted row ID
            emp_id = self.db_manager.last_row_id()

            fquery = """
                INSERT INTO finger_point_scan (emp_id, LL, LR, LM, LI, LT, RL, RR, RM, RI, RT) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            fparams = (
                emp_id, employee.fps.ll, employee.fps.lr, employee.fps.lm, employee.fps.li, employee.fps.lt,
                employee.fps.rl, employee.fps.rr, employee.fps.rm, employee.fps.ri, employee.fps.rt)
            self.db_manager.execute_query_without_commit(fquery, fparams)

            # Commit transaction if all queries succeed
            self.db_manager.commit_transaction()
            print("Transaction committed successfully")
        except Exception as e:
            # Rollback transaction if any error occurs
            self.db_manager.rollback_transaction()
            print("Transaction rolled back due to error:", e)

    def update_employee(self, employee_id, updated_employee):
        try:
            # Begin transaction
            self.db_manager.begin_transaction()

            # Update employee information
            update_query = """
                UPDATE employee 
                SET client_emp_id = ?, emp_name = ?, emp_dob = ?, rf_id = ?, 
                    face_id = ?, mesh_id = ?, role_id = ?, emp_image = ?
                WHERE emp_id = ?
            """
            update_params = (updated_employee.client_emp_id, updated_employee.emp_name, 
                            updated_employee.emp_dob, updated_employee.rf_id,
                            updated_employee.face_id, updated_employee.mesh_id, 
                            updated_employee.role_id, updated_employee.emp_image, 
                            employee_id)
            self.db_manager.execute_query_without_commit(update_query, update_params)

            # Update finger_point_scan information (assuming it's a one-to-one relationship)
            update_fps_query = """
                UPDATE finger_point_scan 
                SET LL = ?, LR = ?, LM = ?, LI = ?, LT = ?, 
                    RL = ?, RR = ?, RM = ?, RI = ?, RT = ?
                WHERE emp_id = ?
            """
            update_fps_params = (updated_employee.fps.ll, updated_employee.fps.lr, 
                                updated_employee.fps.lm, updated_employee.fps.li, 
                                updated_employee.fps.lt, updated_employee.fps.rl, 
                                updated_employee.fps.rr, updated_employee.fps.rm, 
                                updated_employee.fps.ri, updated_employee.fps.rt, 
                                employee_id)
            self.db_manager.execute_query_without_commit(update_fps_query, update_fps_params)

            # Commit transaction if all queries succeed
            self.db_manager.commit_transaction()
            print("Transaction committed successfully")
        except Exception as e:
            # Rollback transaction if any error occurs
            self.db_manager.rollback_transaction()
            print("Transaction rolled back due to error:", e)

    def delete_employee(self, emp_id):   # checkbox status to be checked and deteled accordingly.
        query = "DELETE FROM employee WHERE emp_id=?"
        params = (emp_id,)
        self.db_manager.execute_query(query, params)

    def delete_employee_rfid_fps_face_photo(self, emp_id, is_rfid, is_fps, is_face, is_photo):
        query = """
            UPDATE employee
            SET rf_id = CASE WHEN ? THEN NULL ELSE rf_id END,
                face_id = CASE WHEN ? THEN NULL ELSE face_id END,
                emp_image = CASE WHEN ? THEN NULL ELSE emp_image END
            WHERE client_emp_id=?
        """
        params = (is_rfid, is_face, is_photo, emp_id)
        self.db_manager.execute_query(query, params)

    def verify_employee_client_emp_id(self, client_emp_id):
        query = "SELECT * FROM employee WHERE client_emp_id=?"
        params = (client_emp_id,)
        result = self.db_manager.fetch_data(query, params)
        if result:
            return True
        else:
            return False
    
    def verify_employee_rf_id(self, rf_id):
        query = "SELECT * FROM employee WHERE rf_id=?"
        params = (rf_id,)
        result = self.db_manager.fetch_data(query, params)
        if result:
            return True
        else:
            return False

    def verify_employee_fps(self, fps):
        query = "SELECT * FROM finger_point_scan WHERE LL=? OR LR=? OR LM=? OR LI=? OR LT=? OR RL=? OR RR=? OR RM=? OR RI=? OR RT=?"
        params = (fps, fps, fps, fps, fps, fps, fps, fps, fps, fps)
        result = self.db_manager.fetch_data(query, params)
        if result:
            return True
        else:
            return False

    # def get_employee_by_id(self, client_emp_id):
    #     query = "SELECT * FROM employee WHERE client_emp_id=?"
    #     params = (client_emp_id,)
    #     result = self.db_manager.fetch_data(query, params)
    #     if result:
    #         return self._create_employee_instance(result[0])
    #     return None
    
    def get_employee_by_id(self, client_emp_id):
        query = "SELECT * FROM employee WHERE client_emp_id=?"
        params = (client_emp_id,)
        result = self.db_manager.fetch_data(query, params)
        if result:
            emp_id, client_emp_id, emp_name, emp_dob, rf_id, face_id, mesh_id, role_id, emp_image = result[0]
    
            query1 = "SELECT * FROM finger_point_scan WHERE emp_id=?"
            params1 = (emp_id,)
            result1 = self.db_manager.fetch_data(query1, params1)
            
            if result1:
                fp_id, emp_id, LL, LR, LM, LI, LT, RL, RR, RM, RI, RT = result1[0]
        
                if result1:
                    return Employee(
                        emp_id,
                        client_emp_id,
                        emp_name,
                        emp_dob,
                        rf_id,
                        FingerPointScan(fp_id, emp_id, LL, LR, LM, LI, LT, RL, RR, RM, RI, RT),
                        face_id,
                        mesh_id,
                        role_id,
                        emp_image)
            
        return None
            

    def get_all_employees(self, page=1, page_size=10, sort_by=None, search=None):
        offset = (page - 1) * page_size
        query = "SELECT * FROM employee"
        params = ()

        if search:
            query += " WHERE emp_name LIKE ?"
            params = (f"%{search}%",)

        if sort_by:
            query += f" ORDER BY {sort_by}"

        query += f" LIMIT {page_size} OFFSET {offset}"

        result = self.db_manager.fetch_data(query, params)
        return [self._create_employee_instance(row) for row in result]

    def get_all_employees_by_search_text(self, search_text):
        query = "SELECT *  \
                            FROM employee \
                            WHERE emp_id LIKE ? OR client_emp_id LIKE ? OR \
                            emp_name LIKE ? OR emp_dob LIKE ? OR rf_id LIKE ?"
        params = (f'%{search_text}%', f'%{search_text}%', f'%{search_text}%', f'%{search_text}%', f'%{search_text}%')

        result = self.db_manager.fetch_data(query, params)
        return [self._create_employee_instance(row) for row in result]

    def _create_employee_instance(self, row):
        emp_id, client_emp_id, emp_name, emp_dob, rf_id, face_id, mesh_id, role_id, emp_image = row
        return Employee(emp_id, client_emp_id, emp_name, emp_dob, rf_id, None, face_id, mesh_id, role_id, emp_image)

    def close_connection(self):
        self.db_manager.close_connection()

    def start_connection(self):
        self.db_manager.create_connection()
