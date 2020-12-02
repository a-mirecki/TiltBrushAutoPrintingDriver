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

    LOGPIXELSX = 88
    LOGPIXELSY = 90

    PHYSICALWIDTH = 110
    PHYSICALHEIGHT = 111

    PHYSICALOFFSETX = 0
    PHYSICALOFFSETY = 0

    printer_name = win32print.GetDefaultPrinter ()

    hDC = win32ui.CreateDC ()
    hDC.CreatePrinterDC (printer_name)
    printable_area = hDC.GetDeviceCaps (HORZRES), hDC.GetDeviceCaps (VERTRES)
    printer_size = hDC.GetDeviceCaps (PHYSICALWIDTH), hDC.GetDeviceCaps (PHYSICALHEIGHT)
    printer_margins = hDC.GetDeviceCaps (PHYSICALOFFSETX), hDC.GetDeviceCaps (PHYSICALOFFSETY)

    bmp = Image.open (file_name)
    if bmp.size[0] > bmp.size[1]:
      bmp = bmp.rotate (0)
    watermark = Image.open('ramka.png')
    bmp.paste(watermark, (0, 0, 1080, 1920), watermark)

    ratios = [1.2 * printable_area[0] / bmp.size[0], 1.2 * printable_area[1] / bmp.size[1]]

    print(ratios)
    scale = min (ratios)

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
photo_time = int(time.time()-100)
print(before)

while True:
    time.sleep(1)
    after = dict ([(f, None) for f in os.listdir(path_to_watch)])
    added = [f for f in after if not f in before]
    if added:
        if time.time()-photo_time > 60:
            photo_time = time.time()
            print(" drukuje " + str(added[0]))
            printPhotoFromFilename(str(added[0]))
    before = after