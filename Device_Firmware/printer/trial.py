from escpos.printer import Usb

def print_text(text):
    # Connect to the printer using the USB port
    p = Usb(0x0fe6, 0x811e)  # Replace with the correct vendor and product IDs of your printer

    # Set the text size and alignment
    p.set(align='center', text_type='normal', width=1, height=1)

    # Print the text
    p.text(text)

    # Cut the paper (optional)
    p.cut()

    # Close the connection
    p.close()

# Example usage
text_to_print = "Hello, World!"
print_text(text_to_print)
