import serial
import time

import numpy as np

from flippydot import Panel

# Setup our serial port connection
ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=57600,
    timeout=1,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

# Configure our FlipDot panel
panel = Panel([
    [1],
    [2],
    [3],
    [4],
], 28, 7, module_rotation=0, screen_preview=True)

frame_delay = 0.1

print("Panel width: {}".format(panel.get_total_width()))
print("Panel height: {}".format(panel.get_total_height()))

while 1:

    # Turn entire screen from black to white 10 times
    for i in range(10):
        # Set whole panel to black
        frame = np.zeros((panel.get_total_height(), panel.get_total_width()), dtype=np.uint8)
        serial_data = panel.apply_frame(frame)
        ser.write(serial_data)
        time.sleep(frame_delay)
        # Set whole panel to white
        frame = np.ones((panel.get_total_height(), panel.get_total_width()), dtype=np.uint8)
        serial_data = panel.apply_frame(frame)
        ser.write(serial_data)
        time.sleep(frame_delay)

    # Move a horizontal line across the panel
    for i in range(panel.get_total_width()):
        frame = np.zeros((panel.get_total_height(), panel.get_total_width()), dtype=np.uint8)
        frame[:, i] = 1
        serial_data = panel.apply_frame(frame)
        ser.write(serial_data)
        time.sleep(frame_delay)

    # Display a checkerboard pattern on the screen, and then invert the pattern 10 times
    for i in range(10):
        frame = np.zeros((panel.get_total_height(), panel.get_total_width()), dtype=np.uint8)
        frame[1::2, ::2] = 1
        frame[::2, 1::2] = 1
        serial_data = panel.apply_frame(frame)
        ser.write(serial_data)
        time.sleep(frame_delay)
        frame = np.ones((panel.get_total_height(), panel.get_total_width()), dtype=np.uint8)
        frame[1::2, ::2] = 0
        frame[::2, 1::2] = 0
        serial_data = panel.apply_frame(frame)
        ser.write(serial_data)
        time.sleep(frame_delay)

    # Move a vertical line down the panel
    for i in range(panel.get_total_height()):
        frame = np.zeros((panel.get_total_height(), panel.get_total_width()), dtype=np.uint8)
        frame[i, :] = 1
        serial_data = panel.apply_frame(frame)
        ser.write(serial_data)
        time.sleep(frame_delay)
