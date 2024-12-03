from db_manager import DBManager
from canlog import CanLog

class CanLogRepository:
    def __init__(self):
        self.db_manager = DBManager()

    def create_canlog(self, canlog):
        query = """
            INSERT INTO canlog (emp_id, log_time, dir_flag, dev_id, menu_id)
            VALUES (?, ?, ?, ?, ?)
        """
        params = (canlog.emp_id, canlog.log_time, canlog.dir_flag, canlog.dev_id, canlog.menu_id)
        self.db_manager.execute_query(query, params)

    def update_canlog(self, canlog):
        query = """
            UPDATE canlog
            SET emp_id=?, log_time=?, dir_flag=?, dev_id=?, menu_id=?
            WHERE log_id=?
        """
        params = (canlog.emp_id, canlog.log_time, canlog.dir_flag, canlog.dev_id, canlog.menu_id,
                  canlog.log_id)
        self.db_manager.execute_query(query, params)

    def delete_canlog(self, log_id):
        query = "DELETE FROM canlog WHERE log_id=?"
        params = (log_id,)
        self.db_manager.execute_query(query, params)

    def get_canlog_by_id(self, log_id):
        query = "SELECT * FROM canlog WHERE log_id=?"
        params = (log_id,)
        result = self.db_manager.fetch_data(query, params)
        if result:
            return self._create_canlog_instance(result[0])
        return None

    def get_all_canlogs(self, page=1, page_size=10):
        offset = (page - 1) * page_size
        query = "SELECT * FROM canlog LIMIT ? OFFSET ?"
        params = (page_size, offset)
        result = self.db_manager.fetch_data(query, params)
        return [self._create_canlog_instance(row) for row in result]

    def _create_canlog_instance(self, row):
        log_id, emp_id, log_time, dir_flag, dev_id, menu_id = row
        return CanLog(log_id, emp_id, log_time, dir_flag, dev_id, menu_id)

    def close_connection(self):
        self.db_manager.close_connection()
