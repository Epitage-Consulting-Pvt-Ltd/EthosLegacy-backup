import os
from fps_m import FPS

# Configuration
SERIAL_PORT = '/dev/ttyUSB0'
BAUDRATE = 9600

# Initialize FPS
fps = FPS(SERIAL_PORT, BAUDRATE)

# Enroll finger
def enroll_finger(fps, enroll_id):
    try:
        print(f"Enrolling finger with ID {enroll_id}")
        fps.enroll_finger(enroll_id)
    except ValueError as e:
        print(f"Error during enrollment: {e}")

# Verify finger
def verify_finger(fps, verify_id):
    try:
        print(f"Verifying finger with ID {verify_id}")
        response = fps.verify_finger(verify_id)
        response.response_print()
    except ValueError as e:
        print(f"Error during verification: {e}")

# Get template and save to file
def get_template(fps, template_id, folder="templates"):
    try:
        print(f"Downloading template with ID {template_id}")
        template = fps.get_template(template_id)
        if not os.path.exists(folder):
            os.makedirs(folder)
        with open(os.path.join(folder, f"{template_id}.tpl"), 'wb') as f:
            f.write(template.packet_bytes)
    except ValueError as e:
        print(f"Error getting template: {e}")

# Set template from file
def set_template(fps, template_id, folder="templates"):
    try:
        print(f"Uploading template with ID {template_id}")
        with open(os.path.join(folder, f"{template_id}.tpl"), 'rb') as f:
            template_bytes = f.read()
        response = fps.set_template(template_bytes)
        response.response_print()
    except ValueError as e:
        print(f"Error setting template: {e}")

# Get entire database
def get_database(fps, folder="database"):
    try:
        print("Downloading entire database")
        database = fps.get_database()
        if not os.path.exists(folder):
            os.makedirs(folder)
        for i, template in enumerate(database):
            with open(os.path.join(folder, f"template_{i}.tpl"), 'wb') as f:
                f.write(template)
    except ValueError as e:
        print(f"Error getting database: {e}")

# Set entire database from folder
def set_database(fps, folder="database"):
    try:
        print("Uploading entire database")
        database = []
        for filename in os.listdir(folder):
            if filename.endswith(".tpl"):
                with open(os.path.join(folder, filename), 'rb') as f:
                    database.append(f.read())
        response = fps.set_database(database)
        response.response_print()
    except ValueError as e:
        print(f"Error setting database: {e}")

# Usage
enroll_finger(fps, enroll_id=1)
verify_finger(fps, verify_id=1)
get_template(fps, template_id=1)
set_template(fps, template_id=1)
get_database(fps)
set_database(fps)

fps.close()
