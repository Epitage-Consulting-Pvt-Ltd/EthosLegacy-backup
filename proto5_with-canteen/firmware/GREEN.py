import time
import board
import neopixel

# LED strip configuration
LED_COUNT = 8  # Number of LEDs in your strip
LED_PIN = board.D12  # GPIO pin where your data line is connected
ORDER = neopixel.GRB  # Color order of your strip (GRB for WS2812B)

# Create NeoPixel object
strip = neopixel.NeoPixel(LED_PIN, LED_COUNT, auto_write=False, pixel_order=ORDER)

# Define the color (in RGB format)
green = (0, 255, 0)

# Function to set all LEDs to a specific color
def set_all_leds(color):
    for i in range(LED_COUNT):
        strip[i] = color
    strip.show()

try:
    # Set all LEDs to green
    set_all_leds(green)
    print("LED ON.")

    # Keep the LEDs on for a while
    time.sleep(5)  # Adjust the duration as needed
    print("LED OFF.")

    # Clear the LED strip
    set_all_leds((0, 0, 0))

except KeyboardInterrupt:
    # Clear the LEDs when the script is interrupted (e.g., with Ctrl+C)
    set_all_leds((0, 0, 0))
