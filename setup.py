import base64
from time import sleep
from os import path
from multiprocessing import Process

import config

from satoshis_place import SatPlaceSocket

from PIL import Image
from os import path
from satoshis_place import allowed_colors
import numpy as np
import math
import qrcode

from qrcode.image.pure import PymagingImage

from image import convert_image

import config

print("Running Satoshis.Place Image Uploader...")

url='https://api.satoshis.place'

height = int(input("Enter image height in pixels: "))
width = int(input("Enter image width in pixels: "))

imgx = int(input("Enter canvas coordinate x: "))
imgy = int(input("Enter canvas coordinate y: "))

satPlaceSocket = SatPlaceSocket()
print("Connecting to API")
filename = "img.png"
print("Converting Image")
cj = convert_image(filename, (height, width), imgx, imgy)
print("Requesting Invoice")
emitResult = satPlaceSocket.emitNewOrder(cj)
if emitResult:
    satPlaceSocket.wait(seconds=5)
    try:
        invoice = satPlaceSocket.receivedInvoice
        print("Invoice received: ")
        print(invoice)
        invoiceexists = True
    except AttributeError:
        print("Failed to get invoice")
    else:
        print("- - -")

if invoiceexists == True:
    print("Rendering QR Code...")
    lninv = invoice.get('paymentRequest')
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
        )
    qr.add_data(lninv)
    qr.make(fit=True)
    qr.print_ascii()
else:
    print('No invoice to render')
