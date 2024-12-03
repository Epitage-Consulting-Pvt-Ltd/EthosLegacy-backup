# ethos-firmware
This project is a Raspberry Pi firmware that incorporates rfid, gt521f52, led strip, printer and speakers control.

## Key Features

- Raspberry Pi firmware
- RFID reader
   - 1.Read
     2.Write
- GT521F52 Fingerprint reader
   - 1.Enroll
     2.Delete
     3.Verify
     4.make_template
     5.set_template
     6.get_template
     7. Download All Templates
     8. List Available Templates
     9. Exit
- LED strip
   - 1.Turn on
     2.Turn on GREEN
     3.Turn on RED
     4.Turn on BLUE
     5.Turn on WHITE
     6.Timer
     7.Turn off
- Printer
   - 1.Print
     2.p.text
     3.p.set
     4.p.cut
     5.p.close

## Getting Started
### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Ashman-Technicals/ethos-backup.git
   ```
2. Install the required dependencies:
   ```bash
   sudo raspi-config
   ```
   
   -On here use the arrow keys to select “5 Interfacing Options“. Once you have this option selected, press Enter.
   -Use the arrow keys to select “P1 Legacy Camera". Once you have this option selected, it will if yopu want to enable the legacy support, select No. This will diisable the legacy camera.
   -Use the arrow keys to select “P4 SPI. Once you have this option selected, press Enter.
   -Use the arrow keys to select “P5 I2C". Once you have this option selected, press Enter.
   -Use the arrow keys to select “P6 Serial Port". Once you have this option selected, press Enter.
   -Use the arrow keys to select “P8 Remote GPIO" . Once you have this option selected, press Enter.
   -Use the arrow keys to select “Yes”. Once you have this option selected, press Enter , it will ask you to reboot.

   ```bash
   sudo apt-get update
   sudo apt-get upgrade
   ```
   
3. Install the required Python packages:
   ```bash
   sudo pip3 install python-escpos
   sudo pip3 install RPi.GPIO
   sudo pip3 install adafruit-circuitpython-neopixel
   sudo pip3 install rpi_ws281x adafruit-circuitpython-neopixel
   sudo pip3 install pygame
   sudo apt install libcamera-apps
	sudo apt install python3-picamera2
   sudo pip3 install opencv-python
   sudo pip3 install flask
   ```
   

## MFRC522 Setup
1.   On your RFID RC522 you will notice that there are 8 possible connections on it, these being SDA (Serial Data Signal), SCK (Serial Clock), MOSI (Master Out Slave In), MISO (Master In Slave Out), IRQ (Interrupt Request), GND (Ground Power), RST (Reset-Circuit) and 3.3v (3.3v Power In). We will need to wire all of these but the IRQ to our Raspberry Pi’s GPIO pins.

      SDA connects to Pin 24.
      SCK connects to Pin 23.
      MOSI connects to Pin 19.
      MISO connects to Pin 21.
      GND connects to Pin 6.
      RST connects to Pin 22.
      3.3v connects to Pin 1.

2.   Run the command:
   ```bash
   sudo python3 read_rfid.py
   ```
   Place the RFID card on the reader and it will print the UID of the card.


## MFRC522 Setup if regular connections do not work:
1.	On the command prompt run command ‘sudo raspi-config’ choose ‘Interface Options’ and enable ‘SPI’, ‘Serial Port’ and ‘remote GPIO’.(/usr/local/lib/python3.9/dist-packages/mfrc522)

2.	Localization Setup – Set WIFI Country.

3.	In the raspberry pi ‘config.txt’(cd /boot/) file add line,
	dtoverlay=spi1-3cs

4.	Install the MFRC library using the command ‘sudo pip3 install mfrc522’.

5.	Install SPI library using the command ‘sudo pip3 install spidev’.

6.	Check if the output of ‘ls /dev/spi*’. Expected output - /dev/spidev1.0/1.1/1.2…

7.	Upgrade MFRC library using command ‘sudo python3 -m pip install mfrc522 –upgrade’.

8.	Reboot.

9.	Changes in mfrc.py file. Path for the file ‘cd/user/local/lib/python3.9/dist.packages/mfrc.py. 
Change SPI bus to (1,0).

https://github.com/lthiery/SPI-Py
https://github.com/mxgxw/MFRC522-python/tree/master


### Fingerprint Setup
1. Connect the fingerprint sensor to the Raspberry Pi using the usb port.
2. Check the  fingerprint sensor is connected by running the command :
   ```bash
   dmesg | grep tty
   ```
   This should show finngerprint sensor connected to /dev/ttyUSB0.
3. Run the command :
   ```bash
   sudo python3 fps_main.py
   ```
   This should show the fingerprint sensor menu.
   Follow the instructions on the screen to enroll, verify, delete, or exit the program.

### LED Strip Setup
1. Connect the LED strip to the Raspberry Pi using the GPIO pin 12.
2.    Run the command:
   ```bash
   sudo python3 led.py
   ```
   This should show the LED strip menu.
   Select a color:
      1: Red
      2: Green
      3: Blue
      4: Purple
      5: White
      0: Exit
      Enter your choice:
   The entered choice will turn on the corresponding color for 2 seconds,  then turn off. One can change this delay in the code by changing the value of the delay variable.
   ```bash
   time.sleep(2)
   ```

### Printer Setup
1. Connect the printer to the Raspberry Pi using the Rx and Tx pins (Gpio 14 and 15).
2. Run the command:
   ```bash
   sudo python3 printer_default .py
   ```
   This should print the default text.
   To print a different text, change the text variable in the code.


### Camera Setup
1. Connect the camera to the Raspberry Pi using the CSI port.
2. Run the command:
   ```bash
   sudo python3 cameraTest.py
   ```
   This should show the camera feed.
   Enter the ip of raspberry pi in the browser to view the camera feed followed by port number 8080.


### Speaker (better quality)
1. Use MAX98357a ClassD audio ampifier.
2. ```bash
   sudo nano /boot/config.txt
   ```
   
   Uncomment line (remove '#' at the start of line):
   ```bash
   dtparam=i2s=on
   ```
   
   Update line :
   ```bash
   dtpram=audio=off
   ```
   &
   ```bash
   dtoverlay=vc4-kms-v3d,noaudio
   ```

   Add line:
   ```bash
   dtoverlay=hifiberry-dac
   ```

3. ```bash
   sudo apt install -y wget
   pip3 install adafruit-python-shell
   wget https://github.com/adafruit/Raspberry-Pi-Installer-Scripts/raw/main/i2samp.py
   sudo python3 i2samp.py
   ```
   Tyep Y for every question.
   Reboot the system.
   If you face any audio problems, try re-running the script and saying N (disable) the /dev/zero playback service.

4. Update /etc/modprobe.d (if it exists)
   ```bash
   sudo nano /etc/modprobe.d/raspi-blacklist.conf
   ```
   If the file is empty, just skip this step

   However, if you see the following lines:
   ```bash
   blacklist i2c-bcm2708
   blacklist snd-soc-pcm512x
   blacklist snd-soc-wm8804
   ```
   Update the lines by putting a # before each line
   Save by typing Control-X Y <return>


5. Disable headphone audio (if it's set)
   ```bash
   sudo nano /etc/modules
   ```
   If the file is empty, just skip this step

   However, if you see the following line:
   ```bash
   snd_bcm2835
   ```
   Put a # in front of it and save with Control-X Y <return>

6. Create asound.conf file
   ```bash
   sudo nano /etc/asound.conf
   ```

   Copy and paste the following text into the file
   ```bash
   pcm.speakerbonnet {
   type hw card 0
   }

   pcm.dmixer {
      type dmix
      ipc_key 1024
      ipc_perm 0666
      slave {
      pcm "speakerbonnet"
      period_time 0
      period_size 1024
      buffer_size 8192
      rate 44100
      channels 2
      }
   }

   ctl.dmixer {
      type hw card 0
   }

   pcm.softvol {
      type softvol
      slave.pcm "dmixer"
      control.name "PCM"
      control.card 0
   }

   ctl.softvol {
      type hw card 0
   }

   pcm.!default {
      type             plug
      slave.pcm       "softvol"
   }
   ```

   Save by typing Control-X Y <return>
   Reboot the system.

7. Test audio
   ```   
   sudo speaker-test -t
   ```
   If you hear a tone, the audio is working.

8. Run the command:
   ```bash  
   sudo python3 audio.py
   ```

### install pyqt5:
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip python3-dev libqt5gui5 libqt5webkit5 libqt5svg5-dev libqt5core5a -y
pip3 install pyqt5
```

Verify Installation:
```bash
python3
>>> import PyQt5
>>> print(PyQt5.__version__)
```
### install pyqt5-tools:
```bash
sudo pip3 install pyqt5-tools
```