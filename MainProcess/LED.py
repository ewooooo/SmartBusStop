
# import re
import time

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
# from luma.core.virtual import viewport
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT

class LED:
    def __init__(self):
        serial = spi(port=0, device=0, gpio=noop())
        self.device = max7219(serial, width=32, height=32, block_orientation=-90, rotate=1)
    def SET_LED(self,number):
        self.device.show()
        number = number.replace('-', 'l')

        testlen = len(number)

        if testlen == 1:
            with canvas(self.device) as draw:
                text(draw, (4, 4), number[0], fill="white")

        elif testlen == 2:
            with canvas(self.device) as draw:
                text(draw, (4, 4), number[0], fill="white")
                text(draw, (4, 20), number[1], fill="white")

        elif testlen == 3:
            with canvas(self.device) as draw:
                text(draw, (4, 4), number[0], fill="white")
            if number[1] == 'l':
                text(draw, (7, 20), number[1], fill="white", font=proportional(TINY_FONT))
            else:
                text(draw, (4, 20), number[1], fill="white")
            if number[2] == 'l':
                text(draw, (24, 4), number[2], fill="white", font=proportional(TINY_FONT))
            else:
                text(draw, (21, 4), number[2], fill="white")

        elif testlen == 4:
            with canvas(self.device) as draw:
                text(draw, (4, 4), number[0], fill="white")
                if number[1] == 'l':
                    text(draw, (7, 20), number[1], fill="white", font=proportional(TINY_FONT))
                else:
                    text(draw, (4, 20), number[1], fill="white")
                if number[2] == 'l':
                    text(draw, (24, 4), number[2], fill="white", font=proportional(TINY_FONT))
                else:
                    text(draw, (21, 4), number[2], fill="white")
                if number[2] == 'l':
                    text(draw, (24, 20), number[3], fill="white", font=proportional(TINY_FONT))
                else:
                    text(draw, (21, 20), number[3], fill="white")

        elif testlen == 5:
            with canvas(self.device) as draw:
                text(draw, (4, 2), number[0], fill="white")
                if number[1] == 'l':
                    text(draw, (7, 12), number[1], fill="white", font=proportional(TINY_FONT))
                else:
                    text(draw, (4, 12), number[1], fill="white")
                if number[2] == 'l':
                    text(draw, (7, 22), number[2], fill="white", font=proportional(TINY_FONT))
                else:
                    text(draw, (4, 22), number[2], fill="white")
                if number[3] == 'l':
                    text(draw, (24, 3), number[3], fill="white", font=proportional(TINY_FONT))
                else:
                    text(draw, (21, 3), number[3], fill="white")
                if number[4] == 'l':
                    text(draw, (24, 12), number[4], fill="white", font=proportional(TINY_FONT))
                else:
                    text(draw, (21, 12), number[4], fill="white")

        elif testlen == 6:
            with canvas(self.device) as draw:
                text(draw, (4, 2), number[0], fill="white")

                if number[1] == "l":

                    text(draw, (7, 12), number[1], fill="white", font=proportional(TINY_FONT))
                else:
                    text(draw, (4, 12), number[1], fill="white")
                if number[2] == 'l':
                    text(draw, (7, 22), number[2], fill="white", font=proportional(TINY_FONT))
                else:
                    text(draw, (4, 22), number[2], fill="white")
                if number[3] == 'l':
                    text(draw, (24, 3), number[3], fill="white", font=proportional(TINY_FONT))
                else:
                    text(draw, (21, 3), number[3], fill="white")
                if number[4] == 'l':
                    text(draw, (24, 12), number[4], fill="white", font=proportional(TINY_FONT))
                else:
                    text(draw, (21, 12), number[4], fill="white")
                if number[5] == 'l':
                    text(draw, (24, 22), number[5], fill="white", font=proportional(TINY_FONT))
                else:
                    text(draw, (21, 22), number[5], fill="white")

    def OFF_LED(self):
        self.device.clearup()


if __name__ == "__main__":

    led = LED()
    a = 4000
    while True:
        a = a + 1
        led.SET_LED(str(a)+"-1")
        print("led on")
        time.sleep(3)
        led.OFF_LED()
        print("led OFF")
        time.sleep(1)

