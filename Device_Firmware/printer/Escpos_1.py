from escpos.printer import Serial
from time import *
from datetime import date
from datetime import datetime
now = datetime.now()
dt_string = now.strftime("%b/%d/%Y %H:%M:%S")
print("Today's date:", dt_string)
""" 9600 Baud, 8N1, Flow Control Enabled """
p = Serial(devfile='/dev/serial0',
           baudrate=115200,
           bytesize=8,
           parity='N',
           stopbits=1,
           timeout=1.00,
           dsrdtr=True
           )
p.set(
        align="left",
        font="a",
        width=2,
        height=2,
        density=3,
        invert=0,
        smooth=False,
        flip=False, 
    )
p.text("\n")
p.set(
        align="center",
        font="a",
        width=2,
        height=2,
        density=2,
        invert=0,
        smooth=False,
        flip=False,       
    )
p.text("CIRCUIT DIGEST\n")
p.text("AIRPORT ROAD\n")
p.text("LOCATION : JAIPUR\n")
p.text("TEL : 0141222585\n")
p.text("GSTIN : \n")
p.text("Bill No. : \n\n")
p.set(
        align="left",
        font="a",
        width=2,
        height=2,
        density=2,
        invert=0,
        smooth=False,
        flip=False,       
    )
p.text("DATE : ")
p.text(dt_string)
p.text("\n")
p.text("CASHIER : ")
p.text(" ===========================")
p.text("      ITEM   QTY  PRICE    GB")
p.text(" --------------------------")
p.text("IR SENSOR  2  30   60")
p.text("ULTRASONIC  2  80   160")
p.text("RASPBERRY  1  3300   3300")
p.text("ADOPTOR  2  120   240")
p.text(" --------------------------")
p.text("     SUBTOTAL:  3760")
p.text("     DISCOUNT:  0.8")
p.text("     VAT @ 18%: 676.8")
p.text(" ===========================")
p.text("    BILL TOTAL: 4436.8")
p.text("     TENDERD:  0.8")
p.text("     BALANCE: 676.8")
p.text(" --------------------------")
p.text("          THANK YOU")
p.text(" ===========================")
p.set(
        align="center",
        font="a",
        width=2,
        height=2,
        density=2,
        invert=0,
        smooth=False,
        flip=False,       
    )
p.qr("Circuit Digest",native=True,size=12)
p.text("")
p.barcode('123456', 'CODE39')
#if your printer has paper cuting facility then you can use this function
p.cut()
print("done")
