from flippydot import Panel
import numpy as np
import time

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
    for i in range(10):
        frame = np.zeros((panel.get_total_height(), panel.get_total_width()), dtype=np.uint8)
        frame[1::2,::2] = 1
        frame[::2,1::2] = 1
        serial_data = panel.apply_frame(frame)
        time.sleep(frame_delay)
        frame = np.ones((panel.get_total_height(), panel.get_total_width()), dtype=np.uint8)
        frame[1::2,::2] = 0
        frame[::2,1::2] = 0
        serial_data = panel.apply_frame(frame)
        time.sleep(frame_delay)

    for i in range(10):
        frame = np.zeros((panel.get_total_height(), panel.get_total_width()), dtype=np.uint8)
        serial_data = panel.apply_frame(frame)
        time.sleep(frame_delay)
        frame = np.ones((panel.get_total_height(), panel.get_total_width()), dtype=np.uint8)
        serial_data = panel.apply_frame(frame)
        time.sleep(frame_delay)

    for i in range(panel.get_total_width()):
        frame = np.zeros((panel.get_total_height(), panel.get_total_width()), dtype=np.uint8)
        frame[:,i] = 1
        serial_data = panel.apply_frame(frame)
        time.sleep(frame_delay)

    for i in range(panel.get_total_height()):
        frame = np.zeros((panel.get_total_height(), panel.get_total_width()), dtype=np.uint8)
        frame[i,:] = 1
        serial_data = panel.apply_frame(frame)
        time.sleep(frame_delay)
