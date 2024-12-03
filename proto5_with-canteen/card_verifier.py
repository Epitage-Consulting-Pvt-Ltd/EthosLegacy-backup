import sqlite3
from sqliteInterface import SQLiteInterface  # Import your SQLiteInterface class
from mfrc522 import SimpleMFRC522

class CardVerifier:
    def __init__(self, db_name):
        self.db = SQLiteInterface(db_name)
        self.db.connect()

    def verify_card(self, scanned_rfid):
        query = f"SELECT * FROM employee_data WHERE RFID_id = ?"
        result = self.db.execute_query(query, (str(scanned_rfid),))
        return result

    def disconnect(self):
        self.db.disconnect()

# Initialize the SQLite database
db_name = "employee_data.db"

# Initialize the RFID reader
reader = SimpleMFRC522()

try:
    verifier = CardVerifier(db_name)

    while True:
        # Scan the RFID card
        print("Place an RFID card near the reader...")
        scanned_rfid, _ = reader.read()
        print(f"Scanned RFID Card ID: {scanned_rfid}")

        # Verify the scanned card
        result = verifier.verify_card(scanned_rfid)

        if result:
            employee = result[0]
#           print("Employee found:")
#           print(f"Employee ID: {employee['EmployeeID']}")
            print(f"Employee Name: {employee['EmployeeName']}")
#           print(f"Timestamp: {employee['timestamp']}")
        else:
            print("Employee not found in the database.")

        # Ask if you want to scan another card
        another_scan = input("Scan another RFID card (yes/no): ")
        if another_scan.lower() != "yes":
            break

except KeyboardInterrupt:
    pass

finally:
    # Disconnect from the database
    verifier.disconnect()
