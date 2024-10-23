import numpy as np


class FlippyModule:
    content = np.array([], dtype=np.uint8)
    start_bytes_flush = [0x80, 0x83]
    start_bytes_buffer = [0x80, 0x84]
    end_bytes = [0x8F]

    def __init__(self, width, height, address):
        self.width = width
        self.height = height
        self.address = address
        self.content = np.zeros((self.height, self.width), dtype=np.uint8)
        self.content[2][1] = 0x01

    def set_content(self, content):
        self.content = content

    def fetch_serial_command(self, flush=True):
        return np.array(
            np.concatenate((
                self.start_bytes_flush,
                [self.address],
                np.packbits(self.content, axis=0, bitorder='little').squeeze(),
                self.end_bytes
            )),
            dtype=np.uint8
        )
