import win32print
import win32ui
import time
import os
from PIL import Image, ImageWin

path_to_watch = 'C:\\Users\\amire\\OneDrive\\Documents\\Tilt Brush\\Snapshots'

def printPhotoFromFilename(file_name):
    HORZRES = 8
    VERTRES = 10

    file_name = path_to_watch + "\\" + file_name
    #
    # LOGPIXELS = dots per inch
    #
    LOGPIXELSX = 88
    LOGPIXELSY = 90
    #
    # PHYSICALWIDTH/HEIGHT = total area
    #
    PHYSICALWIDTH = 110
    PHYSICALHEIGHT = 111
    #
    # PHYSICALOFFSETX/Y = left / top margin
    #
    PHYSICALOFFSETX = 0
    PHYSICALOFFSETY = 0

    printer_name = win32print.GetDefaultPrinter ()


    #
    # You can only write a Device-independent bitmap
    #  directly to a Windows device context; therefore
    #  we need (for ease) to use the Python Imaging
    #  Library to manipulate the image.
    #
    # Create a device context from a named printer
    #  and assess the printable size of the paper.
    #
    hDC = win32ui.CreateDC ()
    hDC.CreatePrinterDC (printer_name)
    printable_area = hDC.GetDeviceCaps (HORZRES), hDC.GetDeviceCaps (VERTRES)
    printer_size = hDC.GetDeviceCaps (PHYSICALWIDTH), hDC.GetDeviceCaps (PHYSICALHEIGHT)
    printer_margins = hDC.GetDeviceCaps (PHYSICALOFFSETX), hDC.GetDeviceCaps (PHYSICALOFFSETY)

    #
    # Open the image, rotate it if it's wider than
    #  it is high, and work out how much to multiply
    #  each pixel by to get it as big as possible on
    #  the page without distorting.
    #
    bmp = Image.open (file_name)
    if bmp.size[0] > bmp.size[1]:
      bmp = bmp.rotate (0)
    watermark = Image.open('ramka.png')
    bmp.paste(watermark, (0, 0, 1080, 1920), watermark)

    ratios = [1.2 * printable_area[0] / bmp.size[0], 1.2 * printable_area[1] / bmp.size[1]]

    print(ratios)
    scale = min (ratios)

    #
    # Start the print job, and draw the bitmap to
    #  the printer device at the scaled size.
    #
    hDC.StartDoc (file_name)
    hDC.StartPage ()

    dib = ImageWin.Dib (bmp)
    scaled_width, scaled_height = [int (scale * i) for i in bmp.size]
    x1 = int ((printer_size[0] - scaled_width) / 2)
    y1 = int ((printer_size[1] - scaled_height) / 2)
    x2 = x1 + scaled_width
    y2 = y1 + scaled_height
    dib.draw (hDC.GetHandleOutput (), (x1, y1, x2, y2))

    hDC.EndPage ()
    hDC.EndDoc ()
    hDC.DeleteDC ()

before = dict ([(f, None) for f in os.listdir(path_to_watch)])
czaszdjecia = int(time.time()-100)
print(before)

while True:
    time.sleep(1)
    after = dict ([(f, None) for f in os.listdir(path_to_watch)])
    added = [f for f in after if not f in before]
    if added:
        if time.time()-czaszdjecia > 60:
            czaszdjecia = time.time()
            print(" drukuje " + str(added[0]))
            printPhotoFromFilename(str(added[0]))
    before = after