import board
import neopixel
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

class LEDStripController:
    def __init__(self, pin=board.D12, count=8, order=neopixel.GRB, brightness=0.5):
        self.LED_COUNT = count
        self.LED_PIN = pin
        self.ORDER = order
        self.brightness = brightness

    # Create an instance of the LEDStripController class
        # self.led_controller = LEDStripController(
            # self.LED_PIN, self.LED_COUNT, self.ORDER)
        self.strip = neopixel.NeoPixel(
            self.LED_PIN, self.LED_COUNT, auto_write=False, pixel_order=self.ORDER, brightness=self.brightness)

    def set_red(self):
        for i in range(self.LED_COUNT):
            self.strip[i] = (255, 0, 0)
        self.strip.show()

    def set_green(self):
        for i in range(self.LED_COUNT):
            self.strip[i] = (0, 255, 0)
        self.strip.show()

    def set_blue(self):
        for i in range(self.LED_COUNT):
            self.strip[i] = (0, 0, 255)
        self.strip.show()

    def set_purple(self):
        for i in range(self.LED_COUNT):
            self.strip[i] = (128, 0, 128)
        self.strip.show()

    def set_orange(self):
        for i in range(self.LED_COUNT):
            self.strip[i] = (255, 168, 0)
        self.strip.show()

    def clear_leds(self):
        for i in range(self.LED_COUNT):
            self.strip[i] = (0, 0, 0)
        self.strip.show()