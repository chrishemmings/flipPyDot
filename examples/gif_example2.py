from flippydot import *
import numpy as np
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import time, os, serial

ser = serial.Serial(
	port='/dev/ttyUSB0',
	baudrate=57600,
	timeout=1,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS
)

panel = flippydot.Panel([
    [10, 9, 8, 7, 6, 5, 4, 3, 2, 1],
], 28, 7, module_rotation=90, screen_preview=True)

print("Panel width: {}".format(panel.get_total_width()))
print("Panel height: {}".format(panel.get_total_height()))

frame = Image.open("{}/resources/bubbles_70x28.gif".format(os.path.dirname(os.path.realpath(__file__))))
nframes = 0

while frame:
    np_im=np.array(frame.copy().getdata(),dtype=np.uint8).reshape(frame.size[1], frame.size[0])
    serial_data = panel.apply_frame(np_im)
    ser.write(serial_data)
    time.sleep(.1)

    nframes += 1
    try:
    	frame.seek(nframes)
    except EOFError:
    	frame.seek(0)
    	nframes = 0
