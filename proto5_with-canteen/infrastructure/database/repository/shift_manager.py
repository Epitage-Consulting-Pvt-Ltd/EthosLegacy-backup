from db_manager import DBManager
from shift import Shift

class ShiftRepository:
    def __init__(self):
        self.db_manager = DBManager()

    def create_shift(self, shift):
        query = """
            INSERT INTO shift (shift_name, from_time, to_time)
            VALUES (?, ?, ?)
        """
        params = (shift.shift_name, shift.from_time, shift.to_time)
        self.db_manager.execute_query(query, params)

    def update_shift(self, shift):
        query = """
            UPDATE shift
            SET shift_name=?, from_time=?, to_time=?
            WHERE shift_id=?
        """
        params = (shift.shift_name, shift.from_time, shift.to_time, shift.shift_id)
        self.db_manager.execute_query(query, params)

    def delete_shift(self, shift_id):
        query = "DELETE FROM shift WHERE shift_id=?"
        params = (shift_id,)
        self.db_manager.execute_query(query, params)

    def get_shift_by_id(self, shift_id):
        query = "SELECT * FROM shift WHERE shift_id=?"
        params = (shift_id,)
        result = self.db_manager.fetch_data(query, params)
        if result:
            return self._create_shift_instance(result[0])
        return None

    def get_all_shifts(self, page=1, page_size=10):
        offset = (page - 1) * page_size
        query = "SELECT * FROM shift LIMIT ? OFFSET ?"
        params = (page_size, offset)
        result = self.db_manager.fetch_data(query, params)
        return [self._create_shift_instance(row) for row in result]

    def _create_shift_instance(self, row):
        shift_id, shift_name, from_time, to_time = row
        return Shift(shift_id, shift_name, from_time, to_time)

    def close_connection(self):
        self.db_manager.close_connection()
