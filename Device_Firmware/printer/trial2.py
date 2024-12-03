import usb.core
import usb.util

# USB vendor and product IDs for the thermal printer
vendor_id = 0x0fe6
product_id = 0x811e

# Find the USB device based on vendor and product IDs
device = usb.core.find(idVendor=vendor_id, idProduct=product_id)

if device is None:
    raise ValueError("USB device not found.")

# Open the device and claim the interface
device.set_configuration()
endpoint = device[0][(0, 0)][0]

# Command codes for setting character size and autocutter
SET_CHARACTER_SIZE = b'\x1D\x21'  # GS ! n
AUTOCUTTER = b'\x1D\x56\x00'  # GS V m

# Function to send a command to the printer
def send_command(data):
    device.write(endpoint.bEndpointAddress, data)

# Function to print a message with specified font size and cut the paper
def print_message(message, font_width, font_height):
    # Set character size
    size_command = SET_CHARACTER_SIZE + bytes([font_width | (font_height << 4)])
    send_command(size_command)

    # Print the message
    send_command(message.encode())

    # Cut the paper using the autocutter
    send_command(AUTOCUTTER)

# Example usage: Print a message with font size 1x1 and cut the paper
message = "Hello, World!"
font_width = 1
font_height = 1
print_message(message, font_width, font_height)

# Close the device
usb.util.dispose_resources(device)
