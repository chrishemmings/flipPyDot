import os
import serial
import time

import numpy as np
from PIL import Image

from flippydot import Panel

ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=57600,
    timeout=1,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

panel = Panel([
    [1],
    [2],
    [3],
    [4]
], 28, 7, module_rotation=0, screen_preview=True)

print("Panel width: {}".format(panel.get_total_width()))
print("Panel height: {}".format(panel.get_total_height()))

frame = Image.open("{}/resources/bubbles_28x28.gif".format(os.path.dirname(os.path.realpath(__file__))))
frame_number = 0

while frame:
    type1_frame = frame.copy().convert("1")
    np_im = np.array(type1_frame.getdata(), dtype=np.uint8).reshape(frame.size[1], frame.size[0])
    serial_data = panel.apply_frame(np_im)
    ser.write(serial_data)
    time.sleep(.1)

    frame_number += 1
    try:
        frame.seek(frame_number)
    except EOFError:
        frame.seek(0)
        frame_number = 0
