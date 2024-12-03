from db_manager import DBManager
from infrastructure.database.entity.finger_point_scan import FingerPointScan

class FingerPointScanRepository:
    def __init__(self):
        self.db_manager = DBManager()

    def create_finger_point_scan(self, finger_point_scan):
        query = """
            INSERT INTO finger_point_scan (emp_id, LL, LR, LM, LI, LT, RL, RR, RM, RI, RT)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (finger_point_scan.emp_id, finger_point_scan.LL, finger_point_scan.LR,
                  finger_point_scan.LM, finger_point_scan.LI, finger_point_scan.LT,
                  finger_point_scan.RL, finger_point_scan.RR, finger_point_scan.RM,
                  finger_point_scan.RI, finger_point_scan.RT)
        self.db_manager.execute_query(query, params)

    def update_finger_point_scan(self, finger_point_scan):
        query = """
            UPDATE finger_point_scan
            SET emp_id=?, LL=?, LR=?, LM=?, LI=?, LT=?, RL=?, RR=?, RM=?, RI=?, RT=?
            WHERE fp_id=?
        """
        params = (finger_point_scan.emp_id, finger_point_scan.LL, finger_point_scan.LR,
                  finger_point_scan.LM, finger_point_scan.LI, finger_point_scan.LT,
                  finger_point_scan.RL, finger_point_scan.RR, finger_point_scan.RM,
                  finger_point_scan.RI, finger_point_scan.RT, finger_point_scan.fp_id)
        self.db_manager.execute_query(query, params)

    def delete_finger_point_scan(self, fp_id):
        query = "DELETE FROM finger_point_scan WHERE fp_id=?"
        params = (fp_id,)
        self.db_manager.execute_query(query, params)

    def get_finger_point_scan_by_id(self, fp_id):
        query = "SELECT * FROM finger_point_scan WHERE fp_id=?"
        params = (fp_id,)
        result = self.db_manager.fetch_data(query, params)
        if result:
            return self._create_finger_point_scan_instance(result[0])
        return None

    def get_all_finger_point_scans(self, page=1, page_size=10):
        offset = (page - 1) * page_size
        query = "SELECT * FROM finger_point_scan LIMIT ? OFFSET ?"
        params = (page_size, offset)
        result = self.db_manager.fetch_data(query, params)
        return [self._create_finger_point_scan_instance(row) for row in result]

    def _create_finger_point_scan_instance(self, row):
        fp_id, emp_id, LL, LR, LM, LI, LT, RL, RR, RM, RI, RT = row
        return FingerPointScan(fp_id, emp_id, LL, LR, LM, LI, LT, RL, RR, RM, RI, RT)

    def close_connection(self):
        self.db_manager.close_connection()
