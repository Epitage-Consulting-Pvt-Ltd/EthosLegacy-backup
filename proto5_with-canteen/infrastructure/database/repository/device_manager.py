from db_manager import DBManager
from device import Device

class DeviceRepository:
    def __init__(self):
        self.db_manager = DBManager()

    def create_device(self, device):
        query = """
            INSERT INTO device (dev_name, sr_no, mac_id, ip_add, dir_flag, def_mode, mesh_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        params = (device.dev_name, device.sr_no, device.mac_id, device.ip_add,
                  device.dir_flag, device.def_mode, device.mesh_id)
        self.db_manager.execute_query(query, params)

    def update_device(self, device):
        query = """
            UPDATE device
            SET dev_name=?, sr_no=?, mac_id=?, ip_add=?, dir_flag=?, def_mode=?, mesh_id=?
            WHERE dev_id=?
        """
        params = (device.dev_name, device.sr_no, device.mac_id, device.ip_add,
                  device.dir_flag, device.def_mode, device.mesh_id, device.dev_id)
        self.db_manager.execute_query(query, params)

    def delete_device(self, dev_id):
        query = "DELETE FROM device WHERE dev_id=?"
        params = (dev_id,)
        self.db_manager.execute_query(query, params)

    def get_device_by_id(self, dev_id):
        query = "SELECT * FROM device WHERE dev_id=?"
        params = (dev_id,)
        result = self.db_manager.fetch_data(query, params)
        if result:
            return self._create_device_instance(result[0])
        return None

    def get_all_devices(self, page=1, page_size=10):
        offset = (page - 1) * page_size
        query = "SELECT * FROM device LIMIT ? OFFSET ?"
        params = (page_size, offset)
        result = self.db_manager.fetch_data(query, params)
        return [self._create_device_instance(row) for row in result]

    def _create_device_instance(self, row):
        dev_id, dev_name, sr_no, mac_id, ip_add, dir_flag, def_mode, mesh_id = row
        return Device(dev_id, dev_name, sr_no, mac_id, ip_add, dir_flag, def_mode, mesh_id)

    def close_connection(self):
        self.db_manager.close_connection()
