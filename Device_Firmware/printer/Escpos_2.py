from escpos.printer import Serial

# Initialize the printer with specific settings
p = Serial(devfile='/dev/serial0',
           baudrate=9600,
           bytesize=8,
           parity='N',
           stopbits=1,
           timeout=3000.00,
           dsrdtr=True)

# Set printer attributes
p.set(
        align="left",    # Text alignment (left)
        font="a",        # Font type ('a' is usually the default)
        width=1,         # Text width (1 is normal width)
        height=1,        # Text height (1 is normal height)
        density=2,       # Print density (2 is a common setting)
        smooth=False,    # Disable smooth font
        flip=False       # Disable text flipping
)

# Print text
p.text("Hello World\n")

# Cut the paper
p.cut(full=True)  # Use "full=True" to leave an empty line after cutting

# Close the printer connection
p.close()
