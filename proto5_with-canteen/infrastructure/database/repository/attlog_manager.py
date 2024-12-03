from db_manager import DBManager
from attlog import AttLog

class AttLogRepository:
    def __init__(self):
        self.db_manager = DBManager()

    def create_attlog(self, attlog):
        query = """
            INSERT INTO attlog (emp_id, log_time, dir_flag, dev_id)
            VALUES (?, ?, ?, ?)
        """
        params = (attlog.emp_id, attlog.log_time, attlog.dir_flag, attlog.dev_id)
        self.db_manager.execute_query(query, params)

    def update_attlog(self, attlog):
        query = """
            UPDATE attlog
            SET emp_id=?, log_time=?, dir_flag=?, dev_id=?
            WHERE log_id=?
        """
        params = (attlog.emp_id, attlog.log_time, attlog.dir_flag, attlog.dev_id, attlog.log_id)
        self.db_manager.execute_query(query, params)

    def delete_attlog(self, log_id):
        query = "DELETE FROM attlog WHERE log_id=?"
        params = (log_id,)
        self.db_manager.execute_query(query, params)

    def get_attlog_by_id(self, log_id):
        query = "SELECT * FROM attlog WHERE log_id=?"
        params = (log_id,)
        result = self.db_manager.fetch_data(query, params)
        if result:
            return self._create_attlog_instance(result[0])
        return None

    def get_all_attlogs(self, page=1, page_size=10):
        offset = (page - 1) * page_size
        query = "SELECT * FROM attlog LIMIT ? OFFSET ?"
        params = (page_size, offset)
        result = self.db_manager.fetch_data(query, params)
        return [self._create_attlog_instance(row) for row in result]

    def _create_attlog_instance(self, row):
        log_id, emp_id, log_time, dir_flag, dev_id = row
        return AttLog(log_id, emp_id, log_time, dir_flag, dev_id)

    def close_connection(self):
        self.db_manager.close_connection()
