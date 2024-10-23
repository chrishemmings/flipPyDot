# FlipPyDot

## A Python FlipDot Controller Library

![more cowbell](https://img.shields.io/badge/more-cowbell-brightgreen) ![licence](https://img.shields.io/pypi/l/flippydot?color=brightgreen) ![downloads](https://img.shields.io/pypi/dm/flippydot?color=brightgreen) ![latest version](https://img.shields.io/pypi/v/flippydot?color=brightgreen)

FlipPyDot is a Python package that can be used to control [AlfaZeta](https://flipdots.com/) FlipDots.  This packages is aimed at controlling their [XY5](https://flipdots.com/en/products-services/flip-dot-boards-xy5/) boards, which can come in a number of different sizes, and are all driven over a RS-485 Serial bus, using a fairly simple [protocol](./resources/Flip_dots_protocols_7x7_7x14_7x28_May_2017.pdf).

![A 10 module wide display, where the modules are rotated 90 degrees](https://github.com/chrishemmings/flipPyDot/blob/master/resources/example_display.gif)

This library can be used as an alternative to the vendor supplied software that is required to be run Windows only.  FlipPyDot can be run on Windows, Linux and MacOS.  As it can be run on Linux, a small single board computer such as a [RaspberryPi](https://www.raspberrypi.org/) can be used as the controller.

The FlipDot boards are controlled via a RS-485 interface, and as such the only hardware that the host computer requires is a USB to RS-485 board.  These can be found very cheaply online, for typically less than $5.  This library has been tested using one of these cheap interface modules and a RaspbreryPi 3b+ but, others combinations may work.

![A real cheap USB to RS-485 converter board](https://github.com/chrishemmings/flipPyDot/blob/master/resources/usb_to_rs485_sm.jpg)

## Usage

A number of [examples](https://github.com/chrishemmings/flipPyDot/tree/master/examples) are included in this repository.  But the basic premise is as follows.

Firstly, install [FlipPyDot](https://github.com/chrishemmings/flipPyDot)

```console
foo@bar:~$ pip3 install flippydot
```

Optionally, install the [opencv-python](https://pypi.org/project/opencv-python) package which enables FlipPyDot to generate a preview of the panel.  Then, we can create our application, which can start with something like this

```python3

from flippydot import Panel
import numpy as np
import time, serial

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

```

An explanation of the above code is, we firstly, setup a serial port.  Check the location of this, but, it'll usually be something like `/dev/ttyUSB0` on Linux system.

Secondly, we'll instantiate a `Panel` object.  This has 3 required parameters, firstly, the layout of the FlipDot modules and their Bus ID number.  Secondly, the module width, then the module height.  Options parameters of `module_rotation` and `screen_preview` can be passed.  `module_rotation` is how many degrees clockwise the modules are orientated.  The gif of a working display above as it's modules rotated 90 degrees.  The `screen_preview` can be set to `True` if Pythons OpenCV module is installed when the application runs, a preview of the FlipDot display will show on screen.

The first parameter, the layout of the display, is a 2D array.  In the example above, you'll see that there are 4 modules, stacked vertically on top of each other.  The top panel being Bus ID 1 and so forth.

28 wide, by 14 high seem to be the current standard for the AlfaZeta units, although, it's worth noting that they are usually sold as 2 boards in one unit, so even though it's 28x14, it's actually 2 controllers controlling 2 lots of 28x7 boards.

After this initial setup has been completed, it's now time to send data to the FlipDots.

```python3

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

```
Here we can see that we create a [NumPy](https://numpy.org/) array of the panel height x panel width and fill it with zeros.  We use a datatype of unit8, as really, we only want to deal with 1's and 0's.

After we have created this `frame`, we pass this to `panel.apply_frame`.  This returns us back a suitable bytestring that can be sent to the serial port.  If we have previews enabled, the `apply_frame` also generates us a preview of what will be sent to the computer display, which is ideal for debugging.

There are other [examples](./examples) available that show how to display gifs.  Basically, anything that can be read by [Pillow](https://pillow.readthedocs.io/en/stable/), can be shown on the FlipDots panel in a fairly simple way.

## Credits

- [Chris Hemmings](https://github.com/chrishemmings)
- [Lush Digital](https://github.com/LushDigital)
- [All Contributors](https://github.com/chrishemmings/flipPyDot/contributors)

## License

The MIT License (MIT). Please see [License File](https://github.com/chrishemmings/flipPyDot/blob/master/LICENSE) for more information.
