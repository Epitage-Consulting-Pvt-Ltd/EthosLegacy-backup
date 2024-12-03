import RPi.GPIO as GPIO
import mfrc522
import signal

from RFIDDummy import RFIDPromptDummy

continue_reading = True

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print ("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an instance of the MFRC522 class
MIFAREReader = mfrc522.MFRC522()

# Define the expected UID of the tag to be detected
expected_uid = [0x63, 0x43, 0x36, 0x09, 0x46, 0x99]

# This loop keeps checking for RFID tags
while continue_reading:

    # Scan for cards
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # If a card is found
    if status == MIFAREReader.MI_OK:
        print ("Card detected")

        # Get the UID of the card
        (status,uid) = MIFAREReader.MFRC522_SelectTag(MIFAREReader.PICC_READ)

        # If the UID matches the expected UID
        if status == MIFAREReader.MI_OK and uid == expected_uid:
            print ("Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3])+","+str(uid[4])+","+str(uid[5]))
            show_rfid_window(self)
        else:
            print ("Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3])+","+str(uid[4])+","+str(uid[5]))
            print ("Tag does not match expected UID")


def show_rfid_window(self):
    self.show_rfid_window = RFIDPromptDummy()
    self.show_rfid_window.show()
