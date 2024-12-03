from escpos.printer import Serial, Dummy

p = Serial()
d = Dummy()

# create ESC/POS for the print job, this should go really fast
d.text("This is my image:\n")
# d.image("funny_cat.png")
d.cut()

# send code to printer
p._raw(d.output)