import codecs
import logging
import signal
import serial
import time
import settings
import os

logging.basicConfig(format="[%(name)s][%(asctime)s] %(message)s")
logger = logging.getLogger("Fingerprint")
logger.setLevel(logging.INFO)

# Create directories for templates and database
os.makedirs('templates', exist_ok=True)
os.makedirs('database', exist_ok=True)

class Fingerprint:
    COMMENDS = {
        'None': 0x00,  # Default value for enum. Scanner will return error if sent this.
        'Open': 0x01,  # Open Initialization
        'Close': 0x02,  # Close Termination
        'UsbInternalCheck': 0x03,  # Check if the connected USB device is valid
        'ChangeBaudrate': 0x04,  # Change UART baud rate
        'SetIAPMode': 0x05,  # Enter IAP Mode. FW Upgrade is available in this mode
        'CmosLed': 0x12,  # Control CMOS LED
        'GetEnrollCount': 0x20,  # Get enrolled fingerprint count
        'CheckEnrolled': 0x21,  # Check if the specified ID is already enrolled
        'EnrollStart': 0x22,  # Start an enrollment
        'Enroll1': 0x23,  # Make 1st template for an enrollment
        'Enroll2': 0x24,  # Make 2nd template for an enrollment
        'Enroll3': 0x25,  # Make 3rd template for an enrollment, merge three templates into one, save merged template to database
        'IsPressFinger': 0x26,  # Check if a finger is placed on the sensor
        'DeleteID': 0x40,  # Delete the fingerprint with the specified ID
        'DeleteAll': 0x41,  # Delete all fingerprints from the database
        'Verify1_1': 0x50,  # Verification of the capture fingerprint image with the specified ID
        'Identify1_N': 0x51,  # Identification of the capture fingerprint image with the database
        'VerifyTemplate1_1': 0x52,  # Verification of a fingerprint template with the specified ID
        'IdentifyTemplate1_N': 0x53,  # Identification of a fingerprint template with the database
        'CaptureFinger': 0x60,  # Capture a fingerprint image(256x256) from the sensor
        'MakeTemplate': 0x61,  # Make template for transmission
        'GetImage': 0x62,  # Download the captured fingerprint image(256x256)
        'GetRawImage': 0x63,  # Capture & Download raw fingerprint image(320x240)
        'GetTemplate': 0x70,  # Download the template of the specified ID
        'SetTemplate': 0x71,  # Upload the template of the specified ID
        'GetDatabaseStart': 0x72,  # Start database download, obsolete
        'GetDatabaseEnd': 0x73,  # End database download, obsolete
        'UpgradeFirmware': 0x80,  # Not supported
        'UpgradeISOCDImage': 0x81,  # Not supported
        'Ack': 0x30,  # Acknowledge.
        'Nack': 0x31  # Non-acknowledge
    }

    PACKET_RES_0 = 0x55
    PACKET_RES_1 = 0xAA
    PACKET_DATA_0 = 0x5A
    PACKET_DATA_1 = 0xA5

    ACK = 0x30
    NACK = 0x31

    def __init__(self, port, baud, timeout=1):
        self.port = port
        self.baud = baud
        self.timeout = timeout
        self.ser = None

    def __del__(self):
        self.close_serial()

    def init(self):
        try:
            self.ser = serial.Serial(self.port, baudrate=self.baud, timeout=self.timeout)
            time.sleep(1)
            connected = self.open_serial()
            if not connected:
                self.ser.close()
                baud_prev = 9600 if self.baud == 115200 else 115200
                self.ser = serial.Serial(self.port, baudrate=baud_prev, timeout=self.timeout)
                if not self.open_serial():
                    raise Exception()
                if self.open():
                    self.change_baud(self.baud)
                    logger.info("The baud rate is changed to %s." % self.baud)
                self.ser.close()
                self.ser = serial.Serial(self.port, baudrate=self.baud, timeout=self.timeout)
                if not self.open_serial():
                    raise Exception()
            logger.info("Serial connected.")
            self.open()
            self._flush()
            self.close()
            return True
        except Exception as e:
            logger.error("Failed to connect to the serial.")
            logger.error(e)
        return False

    def open_serial(self):
        if not self.ser:
            return False
        if self.ser.isOpen():
            self.ser.close()
        self.ser.open()
        time.sleep(0.1)
        connected = self.open()
        if connected is None:
            return False
        if connected:
            self.close()
            return True
        else:
            return False

    def close_serial(self):
        if self.ser:
            self.ser.close()

    def is_connected(self):
        return self.ser and self.ser.isOpen()

    def _flush(self):
        while self.ser.readable() and self.ser.inWaiting() > 0:
            p = self.ser.read(self.ser.inWaiting())
            if p == b'':
                break

    def _read(self):
        if self.ser and self.ser.readable():
            try:
                p = self.ser.read()
                if p == b'':
                    return None
                return int(codecs.encode(p, 'hex_codec'), 16)
            except:
                return None
        else:
            return None

    def _read_header(self):
        if self.ser and self.ser.readable():
            firstbyte = self._read()
            secondbyte = self._read()
            return firstbyte, secondbyte
        return None, None

    def _send_packet(self, cmd, param=0):
        try:
            cmd = Fingerprint.COMMENDS[cmd]
            param = [int(hex(param >> i & 0xFF), 16) for i in (0, 8, 16, 24)]

            packet = bytearray(12)
            packet[0] = 0x55
            packet[1] = 0xAA
            packet[2] = 0x01
            packet[3] = 0x00
            packet[4] = param[0]
            packet[5] = param[1]
            packet[6] = param[2]
            packet[7] = param[3]
            packet[8] = cmd & 0x00FF
            packet[9] = (cmd >> 8) & 0x00FF
            chksum = sum(bytes(packet[:10]))
            packet[10] = chksum & 0x00FF
            packet[11] = (chksum >> 8) & 0x00FF
            
            if self.ser and self.ser.writable():
                logger.debug(f"Sending packet: {packet.hex()}")
                self.ser.write(packet)
                return True
            else:
                logger.error("Serial port not writable.")
                return False
        except Exception as e:
            logger.error(f"Exception in _send_packet: {e}")
            return False

    def _read_packet(self, wait=True):
        packet = bytearray(12)
        while True:
            firstbyte, secondbyte = self._read_header()
            if not firstbyte or not secondbyte:
                if wait:
                    continue
                else:
                    return None, None, None, None
            elif firstbyte == Fingerprint.PACKET_RES_0 and secondbyte == Fingerprint.PACKET_RES_1:
                break
        packet[0] = firstbyte
        packet[1] = secondbyte
        p = self.ser.read(10)
        packet[2:12] = p[:]
        logger.debug(f"Received packet header: {packet.hex()}")

        ack = packet[8] == Fingerprint.ACK

        param = bytearray(4)
        param[:] = packet[4:8]
        param = int(codecs.encode(param[::-1], 'hex_codec'), 16)

        res = bytearray(2)
        res[:] = packet[8:10]
        res = int(codecs.encode(res[::-1], 'hex_codec'), 16)

        data = None
        if self.ser and self.ser.readable() and self.ser.inWaiting() > 0:
            firstbyte, secondbyte = self._read_header()
            if firstbyte == Fingerprint.PACKET_DATA_0 and secondbyte == Fingerprint.PACKET_DATA_1:
                data = bytearray()
                data.extend([firstbyte, secondbyte])
                while True:
                    n = self.ser.inWaiting()
                    p = self.ser.read(n)
                    if len(p) == 0:
                        break
                    data.extend(p)
                if len(data) > 2:
                    data = bytes(data[::-1])
                else:
                    data = None  # Ensure data is None if only headers were received.

        logger.debug(f"ACK: {ack}, PARAM: {param}, RES: {res}, DATA: {data}")
        return ack, param, res, data


    def open(self):
        if self._send_packet("Open"):
            ack, _, _, _ = self._read_packet(wait=False)
            return ack
        return None

    def close(self):
        if self._send_packet("Close"):
            ack, _, _, _ = self._read_packet()
            return ack
        return None

    def set_led(self, on):
        if self._send_packet("CmosLed", 1 if on else 0):
            ack, _, _, _ = self._read_packet()
            return ack
        return None

    def get_enrolled_cnt(self):
        if self._send_packet("GetEnrollCount"):
            ack, param, _, _ = self._read_packet()
            return param if ack else -1
        return None

    def is_finger_pressed(self):
        self.set_led(True)
        if self._send_packet("IsPressFinger"):
            ack, param, _, _ = self._read_packet()
            self.set_led(False)
            if not ack:
                return None
            return param == 0
        return None

    def change_baud(self, baud=115200):
        if self._send_packet("ChangeBaudrate", baud):
            ack, _, _, _ = self._read_packet()
            return ack
        return None

    def capture_finger(self, best=False):
        self.set_led(True)
        param = 0 if not best else 1
        if self._send_packet("CaptureFinger", param):
            ack, _, _, _ = self._read_packet()
            self.set_led(False)
            return ack
        return None

    def start_enroll(self, idx):
        if self._send_packet("EnrollStart", idx):
            ack, _, _, _ = self._read_packet()
            return ack
        return None

    def enroll1(self):
        if self._send_packet("Enroll1"):
            ack, _, _, _ = self._read_packet()
            return ack
        return None

    def enroll2(self):
        if self._send_packet("Enroll2"):
            ack, _, _, _ = self._read_packet()
            return ack
        return None

    def enroll3(self):
        if self._send_packet("Enroll3"):
            ack, _, _, _ = self._read_packet()
            return ack
        return None

    def enroll(self, idx=None, try_cnt=10, sleep=1):
        for i in range(try_cnt):
            idx = self.identify()
            if idx is not None:
                break
            time.sleep(sleep)
            logger.info("Checking existence...")
        if idx is not None and idx >= 0:
            return -1

        self.open()
        idx = self.get_enrolled_cnt()
        logger.info("Enroll with the ID: %s" % idx)
        if idx < 0:
            return -1

        logger.info("Start enrolling...")
        cnt = 0
        while not self.start_enroll(idx):
            cnt += 1
            if cnt >= try_cnt:
                return -1
            time.sleep(sleep)

        for enr_num, enr in enumerate(["enroll1", "enroll2", "enroll3"]):
            logger.info("Start %s..." % enr)
            cnt = 0
            while not self.capture_finger():
                cnt += 1
                if cnt >= try_cnt:
                    return -1
                time.sleep(sleep)
                logger.info("Capturing a fingerprint...")
            cnt = 0
            while not getattr(self, enr)():
                cnt += 1
                if cnt >= try_cnt:
                    return -1
                time.sleep(sleep)
                logger.info("Enrolling the captured fingerprint...")
        return idx

    def delete(self, idx=None):
        if idx is None:
            res = self._send_packet("DeleteAll")
        else:
            res = self._send_packet("DeleteID", int(idx))
        if res:
            ack, _, _, _ = self._read_packet()
            return ack
        return None

    def get_template(self, uid):
        if self._send_packet('GetTemplate', idx):
            ack, param, res, data = self._read_packet()
            if ack and data:
                data_bytes = bytearray()
                while self.ser.in_waiting:
                    data_bytes.extend(self.ser.read(self.ser.in_waiting))
                data_bytes = data_bytes[2:]

                # Ensure the get_template directory exists
                os.makedirs("get_template", exist_ok=True)
                # Save template to a file
                filename = f"get_template/template_{idx}.dat"
                with open(filename, "wb") as f:
                    f.write(data_bytes)
                logger.info(f"Template {idx} downloaded and saved as {filename}")
                return True
        return False

    def set_template(self, idx):
        # Ensure the template file exists
        filename = f"get_template/template_{idx}.dat"
        if not os.path.exists(filename):
            logger.error(f"Template file {filename} does not exist.")
            return False
        
        # Read the template data
        with open(filename, "rb") as f:
            data = f.read()
        
        if self._send_packet('SetTemplate', idx):
            packet = bytearray()
            packet.extend([0x5A, 0xA5])
            packet.extend(data)
            self.ser.write(packet)
            ack, _, _, _ = self._read_packet()
            if ack:
                logger.info(f"Template {idx} uploaded successfully.")
                return True
        return False

    def get_database(self):
        logger.info("Starting to get the database...")
        if self._send_packet("GetDatabaseStart"):
            ack, _, _, data = self._read_packet()
            if ack:
                if data:
                    with open('database/database.bin', 'wb') as f:
                        f.write(data)
                    logger.info("Database saved successfully.")
                    return data
                else:
                    logger.error("No data received for database.")
                    return None
            else:
                logger.error("Failed to get database. ACK not received.")
                return None
        else:
            logger.error("Failed to send GetDatabaseStart command.")
            return None

    def set_database(self, filename):
        with open(f'database/{filename}', 'rb') as f:
            database = f.read()
        if self._send_packet("SetTemplate"):
            ack, _, _, _ = self._read_packet()
            return ack
        return None

    def identify(self):
        while not self.capture_finger():
            time.sleep(0.1)
        if self._send_packet("Identify1_N"):
            ack, param, _, _ = self._read_packet()
            return param if ack else -1
        return None
    
    def save_template_to_file(self, uid, template):
        filename = f'templates/template_{uid}.dat'
        with open(filename, 'wb') as f:
            f.write(template)
        logger.info(f"Template for UID {uid} saved to {filename}")

    def load_template_from_file(self, uid):
        filename = f'templates/template_{uid}.dat'
        if os.path.exists(filename):
            with open(filename, 'rb') as f:
                template = f.read()
            logger.info(f"Template for UID {uid} loaded from {filename}")
            return template
        logger.error(f"Template file {filename} does not exist")
        return None


if __name__ == '__main__':
    f = Fingerprint(settings.PORT_FINGERPRINTSCANNER, 115200)

    def signal_handler(signum, frame):
        f.close_serial()
    signal.signal(signal.SIGINT, signal_handler)

    if f.init():
        print("Open: %s" % str(f.open()))

        count = f.get_enrolled_cnt()

        while True:
            print(f"Number of enrolled: {count}")
            print("1. Enroll")
            print("2. Delete")
            print("3. Verify")
            print("4. Get Template")
            print("5. Set Template")
            print("6. Get Database")
            print("7. Set Database")
            print("8. Exit")

            ch = input("Your Choice: ")
            if ch == '1':
                while f.get_enrolled_cnt() != count + 1:
                    time.sleep(0.5)
                    idtemp = f.identify()
                    if idtemp is not None and idtemp >= 0:
                        print(f"You are an already existing User with ID: {idtemp + 1}")
                        break
                    else:
                        if f.capture_finger():
                            f.enroll()
                            time.sleep(0.5)
                            count += 1
                            print("Successfully Enrolled!")
                            break
                        else:
                            print("Please place your finger")
            elif ch == '2':
                did = input("Enter ID number to delete: ")
                if f.delete(did):
                    print(f"Deleted: {did}")
                    count -= 1
                else:
                    print(f"Failed to delete ID: {did}")
            elif ch == '3':
                print("Place your Finger")
                idtemp = f.identify()
                if idtemp == -1:
                    print("You are not a valid user")
                elif idtemp is not None:
                    print(f"You are an existing User with ID: {idtemp + 1}")
                else:
                    print("Did not place finger")
            elif ch == '4':
                idx = int(input("Enter ID to get template: "))
                template = f.get_template(idx)
                if template:
                    print(f"Template for ID {idx} saved successfully.")
                else:
                    print(f"Failed to get template for ID: {idx}")
            elif ch == '5':
                print("Available templates:")
                templates = os.listdir('templates')
                for template in templates:
                    print(template)
                
                idx = int(input("Enter ID to set template: "))
                filename = input("Enter template filename from above list: ")
                if f.set_template(idx, filename):
                    print(f"Template for ID {idx} set successfully.")
                else:
                    print(f"Failed to set template for ID: {idx}")
            elif ch == '6':
                database = f.get_database()
                if database:
                    print("Database saved successfully.")
                else:
                    print("Failed to get database.")
            elif ch == '7':
                filename = input("Enter database filename: ")
                if f.set_database(filename):
                    print("Database set successfully.")
                else:
                    print("Failed to set database.")
            elif ch == '8':
                print("Close: %s" % str(f.close()))
                f.ser.close()
                break
            else:
                print("Invalid choice, please try again.")
