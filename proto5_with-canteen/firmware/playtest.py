import os
import pygame
from queue import Queue
from time import sleep
from rfid_read import RFIDReader

# Initialize Pygame mixer
pygame.mixer.init()

# Define the directory where the program is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Define MP3 files for success and failure
SUCCESS_MP3 = os.path.join(BASE_DIR, "thank-you.mp3")
FAILURE_MP3 = os.path.join(BASE_DIR, "rejected.mp3")

# Function to play MP3 files
def play_audio(file):
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        sleep(0.1)

# Create an instance of RFIDReader
reader = RFIDReader()

# Connect signals to play_audio function
reader.verify_id.employee_verified.connect(lambda: play_audio(SUCCESS_MP3))
print("mp3_1 played")
reader.verify_id.employee_not_verified.connect(lambda: play_audio(FAILURE_MP3))
print("mp3_2 played")

# Main loop (in your actual program, this could be the main loop of your application)
while True:
    # Your main program logic goes here
    pass
