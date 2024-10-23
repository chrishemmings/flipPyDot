import sys

import numpy as np

from .flippymodule import FlippyModule

try:
    import cv2
except Exception:
    # Do nothing, cv2 is not really required and is only used
    # to display the screen preview if the user asks for it
    pass


class Panel:
    valid_module_rotations = [0, 90, 180, 270]
    module_rotation = 0
    module_width = 0
    module_height = 0
    modules = None
    panel_id = 0

    def __init__(self, layout, module_width: int, module_height: int, module_rotation: int = 0,
                 screen_preview: bool = False):
        """
        :param layout: An array structure of the panel layout with panel id's
        :param module_width: Module width, normally 28
        :param module_height: Module height, normally 7
        :param module_rotation: Rotation of the module, i.e 0, 90, 180 or 270
        :param screen_preview: If cv2 is installed, can draw preview on screen
        """
        if 'cv2' not in sys.modules and screen_preview:
            print("Screen preview requested, but cv2 not loaded, previews will not be generated")
            screen_preview = False

        # Check rotation is valid
        if module_rotation not in self.valid_module_rotations:
            raise Exception("module rotation not valid, must be 0, 90, 180 or 270")

        self.module_width = module_width
        self.module_height = module_height
        self.module_rotation = module_rotation
        self.screen_preview = screen_preview

        # Check we have a valid 2D square array as the layout
        if len(np.shape(layout)) != 2:
            raise Exception("panel layout does not equate to a rectangle/square")

        for row in layout:
            module_row = np.array([])

            for cell in row:
                module_row = np.append(module_row, FlippyModule(module_width, module_height, cell))

            if self.modules is None:
                self.modules = np.array([module_row])
            else:
                self.modules = np.concatenate((self.modules, np.array([module_row])), axis=0)

    def get_total_width(self):

        if self.module_rotation == 0 or self.module_rotation == 180:
            return self.module_width * np.shape(self.modules)[1]
        else:
            return self.module_height * np.shape(self.modules)[1]

    def get_total_height(self):

        if self.module_rotation == 0 or self.module_rotation == 180:
            return self.module_height * np.shape(self.modules)[0]
        else:
            return self.module_width * np.shape(self.modules)[0]

    def get_content(self):
        y = None

        for moduleRow in self.modules:
            x = None
            for module in moduleRow:

                if self.module_rotation == 90:
                    module_data = np.rot90(module.content, 1)
                elif self.module_rotation == 180:
                    module_data = np.rot90(module.content, 2)
                elif self.module_rotation == 270:
                    module_data = np.rot90(module.content, 3)
                else:
                    module_data = module.content

                if x is None:
                    x = module_data
                else:
                    x = np.concatenate((x, module_data), axis=1)
            if y is None:
                y = x
            else:
                y = np.concatenate((y, x), axis=0)

        return y

    def draw_preview(self):
        panel_content = self.get_content()
        cv2.imshow('FlipDisc Preview', np.uint8(panel_content * 255))
        cv2.waitKey(1)

    def apply_frame(self, matrix_data):

        # Check shapes match
        # print((self.get_total_height(), self.get_total_width(), 1) == np.shape(matrixData))

        # Split the panel into rows
        row_split_data = np.split(matrix_data, np.shape(self.modules)[0], 0)

        row_count = 0

        for row_data in row_split_data:
            # Split the row verticals (axis=1)
            module_data_split = np.split(row_data, np.shape(self.modules)[1], 1)

            # Loop module data
            column_count = 0
            for module_data in module_data_split:
                # Rotate data if required
                if self.module_rotation == 90:
                    module_data = np.rot90(module_data, 3)
                elif self.module_rotation == 180:
                    module_data = np.rot90(module_data, 2)
                elif self.module_rotation == 270:
                    module_data = np.rot90(module_data, 1)
                else:
                    module_data = module_data
                # Set module content
                self.modules[row_count, column_count].set_content(module_data)
                column_count = column_count + 1
            row_count = row_count + 1

        # Draw screen preview if required
        if self.screen_preview:
            self.draw_preview()

        serial_data = np.array([])

        for moduleRow in self.modules:
            for module in moduleRow:
                output = module.fetch_serial_command()
                serial_data = np.append(serial_data, output.view('S32').squeeze())

        return serial_data
