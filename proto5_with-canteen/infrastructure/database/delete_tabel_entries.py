import sqlite3

# Connect to the SQLite database
db_name = "ethos_firmware.db"
connection = sqlite3.connect(db_name)
cursor = connection.cursor()

# Clear the table
try:
    cursor.execute("DELETE FROM finger_point_scan;")
    connection.commit()
    print("Table cleared successfully!")
except sqlite3.Error as e:
    print(f"Error clearing the table: {e}")
finally:
    # Close the connection
    connection.close()
