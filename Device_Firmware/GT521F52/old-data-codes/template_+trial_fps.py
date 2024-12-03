import codecs
import logging
import serial
import time
import os 

logging.basicConfig(format="[%(name)s][%(asctime)s] %(message)s")
logger = logging.getLogger("Fingerprint")
logger.setLevel(logging.INFO)

class Fingerprint():

    COMMENDS = {
        'None': 0x00,  # Default value for enum. Scanner will return error if sent this.
        'Open': 0x01,  # Open Initialization
        'Close': 0x02,  # Close Termination
        'UsbInternalCheck': 0x03,  # UsbInternalCheck Check if the connected USB device is valid
        'ChangeBaudrate': 0x04,  # ChangeBaudrate Change UART baud rate
        'SetIAPMode': 0x05,  # SetIAPMode Enter IAP Mode In this mode, FW Upgrade is available
        'CmosLed': 0x12,  # CmosLed Control CMOS LED
        'GetEnrollCount': 0x20,  # Get enrolled fingerprint count
        'CheckEnrolled': 0x21,  # Check whether the specified ID is already enrolled
        'EnrollStart': 0x22,  # Start an enrollment
        'Enroll1': 0x23,  # Make 1st template for an enrollment
        'Enroll2': 0x24,  # Make 2nd template for an enrollment
        'Enroll3': 0x25,
        # Make 3rd template for an enrollment, merge three templates into one template, save merged template to the database
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
            print("Failed to connect to the serial.")
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
        if self.ser and self.ser.isOpen():
            return True
        return False

    def _send_packet(self, cmd, param=0):
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
            self.ser.write(packet)
            return True
        else:
            return False

    def _send_data(self, data, parameter=False): 
        if self.ser and self.ser.writable():
            print("length of written data : ", self.ser.write(data))
            time.sleep(0.1)
            print("SENDing DATA ...", end=' ')
            ack, param, _, _ = self._read_packet()
            print("✅")
            if parameter:
                if ack:
                    return param
                return -1
            return ack
        else:
            return False

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

    def _read_packet(self, wait=True):
        """

        :param wait:
        :return: ack, param, res, data
        """
        # Read response packet
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

        # Parse ACK
        ack = True if packet[8] == Fingerprint.ACK else False

        # Parse parameter
        param = bytearray(4)
        param[:] = packet[4:8]
        if param is not None:
            param = int(codecs.encode(param[::-1], 'hex_codec'), 16)

        # Parse response
        res = bytearray(2)
        res[:] = packet[8:10]
        if res is not None:
            res = int(codecs.encode(res[::-1], 'hex_codec'), 16)

        # Read data packet
        data = None
        if self.ser and self.ser.readable() and self.ser.inWaiting() > 0:
            firstbyte, secondbyte = self._read_header()
            if firstbyte and secondbyte:
                # Data exists.
                if firstbyte == Fingerprint.PACKET_DATA_0 and secondbyte == Fingerprint.PACKET_DATA_1:
                    print(">> Data exists...")
                    # print("FB-SB: ", firstbyte, secondbyte)
                    data = bytearray()
                    data.append(firstbyte)
                    data.append(secondbyte)
        read_buffer = b''                    
        if data:
            while True:
                chunk_size = 14400
                p = self.ser.read(size=chunk_size)
                read_buffer += p
                # print(p, type(p))
                if len(p) == 0:
                    print(">> Transmission Completed . . .")
                    break

        return ack, param, res, read_buffer

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
        print("Checking if finger is pressed or not.")
        self.set_led(True)
        time.sleep(1)
        if self._send_packet("IsPressFinger"):
            ack, param, _, _ = self._read_packet()
            self.set_led(False)
            if not ack:
                return None
            return True if param == 0 else False
        else:
            return None

    def change_baud(self, baud=115200):
        if self._send_packet("ChangeBaudrate", baud):
            ack, _, _, _ = self._read_packet()
            return True if ack else False
        return None

    def capture_finger(self, best=False):
        self.set_led(True)
        time.sleep(1)
        param = 0 if not best else 1
        if self._send_packet("CaptureFinger", param):
            ack, _, _, _ = self._read_packet()
            self.set_led(False)
            return ack
        return None

    def GetImage(self):
        '''
            Gets an image that is 258x202 (52116 bytes) and returns it in 407 Data_Packets
            Use StartDataDownload, and then GetNextDataPacket until done
            Returns: True (device confirming download starting)
        '''
        if self._send_packet("GetImage"):
            ack, param, res, data = self._read_packet()
            if not ack:
                return None, False
            return data, True  if param == 0 else False
        else:
            return None, False
    
    def MakeTemplate(self):
        if not self.capture_finger(best=True):
            return None
        if self._send_packet("MakeTemplate"):
            ack, param, res, data = self._read_packet()
            if not ack:
                return None, False
            return data, True  if param == 0 else False
        else:
            return None, False
    
    def get_template(self, idx):
        if self._send_packet("GetTemplate", param=idx):
            ack, param, res, data = self._read_packet()
            if not ack:
                return None, False
            return data, True  if param == 0 else False
        else:
            return None, False

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
            ack, param, res, data = self._read_packet()
            if not ack:
                return None, False
            return data, True  if param == 0 else False
        return None, None

    # def enroll(self, idx=None, try_cnt=10, sleep=1):
    #     if idx >= 0:
    #         # Check whether the finger already exists or not
    #         for i in range(try_cnt):
    #             idx = self.identify()
    #             print("Given id: ", idx)
    #             if idx is not None:
    #                 break
    #             time.sleep(sleep)
    #             logger.info("Checking existence...")
    #         if idx is not None and idx >= 0:
    #             return -1

    #         # Decide an ID for enrolling
    #         self.open()
    #         idx = self.get_enrolled_cnt()
    #     logger.info("Enroll with the ID: %s" % idx)

    #     """Start enrolling
    #     """
    #     logger.info("Start enrolling...")
    #     cnt = 0
    #     while True:
    #         # idx=0
    #         if self.start_enroll(idx):
    #             # Enrolling started
    #             break
    #         else:
    #             cnt += 1
    #             if cnt >= try_cnt:
    #                 return -1
    #             time.sleep(sleep)

    #     """Start enroll 1, 2, and 3
    #     """
    #     for enr_num, enr in enumerate(["enroll1", "enroll2"]):
    #         print("Start %s..." % enr)
    #         cnt = 0
    #         while not self.capture_finger(best=True):
    #             cnt += 1
    #             if cnt >= try_cnt:
    #                 return -1
    #             time.sleep(sleep)
    #             logger.info("Capturing a fingerprint...")
    #         cnt = 0
    #         while not getattr(self, enr)():
    #             cnt += 1
    #             if cnt >= try_cnt:
    #                 return -1
    #             time.sleep(sleep)
    #             logger.info("Enrolling the captured fingerprint...")
            
    #     if self.capture_finger(best=True):
    #         print("Start enroll3...")
    #         data, downloadstat = self.enroll3()
    #         if idx == -1:
    #             return idx, data, downloadstat
    #     # Enroll process finished
    #     return idx, None, None

    def enroll(self, idx=None, try_cnt=10, sleep=1):

        # Check whether the finger already exists or not
        for i in range(try_cnt):
            idx = self.identify()
            if idx is not None:
                break
            time.sleep(sleep)
            logger.info("Checking existence...")
        if idx is not None and idx >= 0:
            return -1

        # Decide an ID for enrolling
        self.open()
        idx = self.get_enrolled_cnt()
        logger.info("Enroll with the ID: %s" % idx)
        if idx < 0:
            return -1

        """Start enrolling
        """
        logger.info("Start enrolling...")
        cnt = 0
        while True:
            if self.start_enroll(idx):
                # Enrolling started
                break
            else:
                cnt += 1
                if cnt >= try_cnt:
                    return -1
                time.sleep(sleep)

        """Start enroll 1, 2, and 3
        """
        for enr_num, enr in enumerate(["enroll1", "enroll2", "enroll3"]):
            logger.info("Start %s..." % enr)

            """
            if enr_num > 0:
                # Wait finger detached
                while not self.is_finger_pressed():
                    time.sleep(sleep)
                    logger.info("Waiting finger detached...")
            """

            cnt = 0
            while not self.capture_finger():             #capture_finger function
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

        # Enroll process finished
        return idx
    
    def verifyTemplate(self, idx, data):
        data_bytes = bytearray()
        data_bytes.append(90)
        data_bytes.append(165)
        for ch in data:
            data_bytes.append(ch)
        if self._send_packet("VerifyTemplate1_1", param=idx):
            ack, _, _, _ = self._read_packet()
            if ack:
                sendstatus = self._send_data(data_bytes)
                if sendstatus:
                    print('|', '>'*10, '👍 MATCH FOUND 👍')
                    return True
                return False

    def setTemplate(self, idx, data):
        data_bytes = bytearray()
        data_bytes.append(90)
        data_bytes.append(165)
        for ch in data:
            data_bytes.append(ch)
        if self._send_packet("SetTemplate", param=idx):
            ack, _, _, _ = self._read_packet()
            if ack:
                if self._send_data(data_bytes):
                    print(f'👍 setTemplate @ ID: {idx}')
                    return True
                return False
            return False
        return False
       
    def delete(self, idx=None):
        res = None
        if idx == None:
        # Delete all fingerprints
            res = self._send_packet("DeleteAll")
        else:
            # Delete all fingerprints
            res = self._send_packet("DeleteID", idx)
        if res:
            ack, _, _, _ = self._read_packet()
            return ack
        return None

    def identify(self):
        if not self.capture_finger(best=True):
            return None
        if self._send_packet("Identify1_N"):
            ack, param, _, _ = self._read_packet()
            if ack:
                return param
            else:
                return -1
        return None

    def identifyTemplate(self, data):
        data_bytes = bytearray()
        data_bytes.append(90)
        data_bytes.append(165)
        for ch in data:
            data_bytes.append(ch)
        if self._send_packet("IdentifyTemplate1_N"):
            ack, _, _, _ = self._read_packet()
            if ack:
                param = self._send_data(data_bytes, parameter=True)
                return param
            return -1
        return None
    
    def list_templates(self):
        templates = [f for f in os.listdir("templates") if f.endswith(".dat")]
        return templates
    
    # def retry_get_template(f, id, retries=5):
    #     for attempt in range(retries):
    #         data, success = f.get_template(id)
    #         if success:
    #             return data, True
    #         else:
    #             print(f"Attempt {attempt + 1} to fetch template for ID {id} failed.")
    #             time.sleep(1)  # Wait a moment before retrying
    #     return None, False

if __name__ == '__main__':

    f = Fingerprint('/dev/ttyUSB0', 115200)
    if not os.path.exists("templates"):
        os.makedirs("templates")
   # f = Fingerprint(settings.ser, 9600)

    # def signal_handler(signum, frame):
    #     f.close_serial()
    # signal.signal(signal.SIGINT, signal_handler)

    if f.init():
        print("Open: %s" % str(f.open()))
        init = f.init()
        print("is initialized :", init)
        
        #f.delete()
        count = f.get_enrolled_cnt()
        
        ch = 0
        while ch != 9:
            print("no : of enrolled : %s" % str(count))
            print("1.Enroll")
            print("2.Delete")
            print("3.Verify")
            print("4.make_template")
            print("5.set_template")
            print("6.get_template")
            print("7. Download All Templates")
            print("8. List Available Templates")
            print("9. Exit")
            f1 = 0
            ch = input("Your Choice:  ")  

            if ch == '1':
                while f.get_enrolled_cnt() != count + 1:
                    time.sleep(0.5)
                    idtemp = str(f.identify())
                    #idtemp = -1
                    if idtemp > "-1" and idtemp != "None":
                        print("You are an already existing User with ID : %s" %(str(idtemp)+str(1)))
                        break
                    else:
                        if f.capture_finger():                      #capture_finger function             
                            f.enroll()
                            time.sleep(0.5)
                            count = count + 1
                            print(" Successfully Enrolled!!!!")
                            break
            
            if ch == '2':
                status = f.delete() # delete all
                print("\n |__ Delete status: ", status)
                # To get total enrollment count
                print(f"\n |__ enrolled counts :", f.get_enrolled_cnt())

            if ch == '3':
                check_finger = f.is_finger_pressed()
                if check_finger == True:
                    id = f.identify()
                    print("\n |__ identified id:", id)
                else:
                    print("\n |__ No finger is pressed")

            if ch == '4':
                data, downloadstat =f.MakeTemplate()
                print(f"\n |__ Is template fetched ?", downloadstat)
                
                img_arr = []
                if downloadstat:
                    data = bytearray(data)
                    for ch in data:
                        img_arr.append(ch)
                print("fetched template data: ", img_arr)

            if ch == '5':
                DATA = [] # a 502 length python list, that we get after running "task 3"
                f.delete(idx=0)
                status = f.setTemplate(idx=0, data=DATA)
                print("\n |__ set template status :", status)

            
            if ch == '6':
                id = int(input("Enter the ID to fetch the template: "))
                data, success = f.get_template(id)
                if data:
                    print(f"Template for ID {id} fetched successfully.")
                    img_arr = list(data)
                    # img_arr = [ch for ch in bytearray(data)]
                    print("Fetched template data:", img_arr)
                    # Save data to a file if needed
                    with open(os.path.join("templates", f"template_{id}.dat"), "wb") as file:
                        file.write(data)
                        # file.write(bytearray(data))
                else:
                    print(f"Failed to fetch template for ID {id}.")

            if ch == '7':
                count = f.get_enrolled_cnt()
                for id in range(count):
                    data, success = f.get_template(id)
                    # data, success = f.retry_get_template(id)
                    if data:
                    # if success:
                        print(f"Template for ID {id} fetched successfully.")
                        with open(os.path.join("templates", f"template_{id}.dat"), "wb") as file:
                            file.write(data)
                    else:
                        print(f"Failed to fetch template for ID {id}.")
                print("All templates downloaded successfully.")

            if ch == '8':
                templates = f.list_templates()
                if templates:
                    print("Available Templates:")
                    for i, template in enumerate(templates):
                        print(f"{i + 1}. {template}")
                    
                    template_choice = input("Select a template to upload or enter 'all' to upload all templates: ")
                    current_count = f.get_enrolled_cnt()  # Check the current count of enrolled templates
                    next_id = current_count  # Set the next ID to be the current count

                    if template_choice.lower() == 'all':
                        for template in templates:
                            with open(os.path.join("templates", template), "rb") as file:
                                data = file.read()
                                # next_id = f.get_enrolled_cnt()
                                status = f.setTemplate(idx=next_id, data=data)
                                if status:
                                    print(f"Template {template} uploaded successfully to ID {next_id}.")
                                    next_id += 1
                                else:
                                    print(f"Failed to upload template {template}.")
                    else:
                        try:
                            template_index = int(template_choice) - 1
                            if 0 <= template_index < len(templates):
                                template = templates[template_index]
                                with open(os.path.join("templates", template), "rb") as file:
                                    data = file.read()
                                    # next_id = f.get_enrolled_cnt()
                                    status = f.setTemplate(idx=next_id, data=data)
                                    if status:
                                        print(f"Template {template} uploaded successfully to ID {next_id}.")
                                        next_id += 1
                                    else:
                                        print(f"Failed to upload template {template}.")
                            else:
                                print("Invalid choice. Please select a valid template number.")
                        except ValueError:
                            print("Invalid input. Please enter a number or 'all'.")
                else:
                    print("No templates available in the 'templates' folder.")

            if ch == '9':
                f.close_serial()
                break