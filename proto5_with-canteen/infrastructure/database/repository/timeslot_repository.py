from db_manager import DBManager
from timeslot import TimeSlot

class TimeSlotRepository:
    def __init__(self):
        self.db_manager = DBManager()

    def create_timeslot(self, timeslot):
        query = """
            INSERT INTO timeslot (timeslot_name, from_time, to_time, shift_id, menugrp_id)
            VALUES (?, ?, ?, ?, ?)
        """
        params = (timeslot.timeslot_name, timeslot.from_time, timeslot.to_time,
                  timeslot.shift_id, timeslot.menugrp_id)
        self.db_manager.execute_query(query, params)

    def update_timeslot(self, timeslot):
        query = """
            UPDATE timeslot
            SET timeslot_name=?, from_time=?, to_time=?, shift_id=?, menugrp_id=?
            WHERE timeslot_id=?
        """
        params = (timeslot.timeslot_name, timeslot.from_time, timeslot.to_time,
                  timeslot.shift_id, timeslot.menugrp_id, timeslot.timeslot_id)
        self.db_manager.execute_query(query, params)

    def delete_timeslot(self, timeslot_id):
        query = "DELETE FROM timeslot WHERE timeslot_id=?"
        params = (timeslot_id,)
        self.db_manager.execute_query(query, params)

    def get_timeslot_by_id(self, timeslot_id):
        query = "SELECT * FROM timeslot WHERE timeslot_id=?"
        params = (timeslot_id,)
        result = self.db_manager.fetch_data(query, params)
        if result:
            return self._create_timeslot_instance(result[0])
        return None

    def get_all_timeslots(self, page=1, page_size=10):
        offset = (page - 1) * page_size
        query = "SELECT * FROM timeslot LIMIT ? OFFSET ?"
        params = (page_size, offset)
        result = self.db_manager.fetch_data(query, params)
        return [self._create_timeslot_instance(row) for row in result]

    def _create_timeslot_instance(self, row):
        timeslot_id, timeslot_name, from_time, to_time, shift_id, menugrp_id = row
        return TimeSlot(timeslot_id, timeslot_name, from_time, to_time, shift_id, menugrp_id)

    def close_connection(self):
        self.db_manager.close_connection()
