import time
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional,TINY_FONT

class LED:
    def __init__(self):
        serial = spi(port=0, device=0, gpio=noop())
        self.device = max7219(serial, width=32, height=32, block_orientation=-90, rotate=1)

    def SET_LED_set(self,number,sel):
        number = number.replace('-', 'l')

        if sel == 1:
            turnColor = "white"
        else :
            turnColor = "black"
        testlen = len(number)

        if testlen == 1:
            with canvas(self.device) as draw:
                text(draw, (4, 4), number[0], fill=turnColor)

        elif testlen == 2:
            with canvas(self.device) as draw:
                text(draw, (4, 4), number[0], fill=turnColor)
                text(draw, (4, 20), number[1], fill=turnColor)

        elif testlen == 3:
            with canvas(self.device) as draw:
                text(draw, (4, 4), number[0], fill=turnColor)
                if number[1] == 'l':
                    text(draw, (7, 20), number[1], fill=turnColor, font=proportional(TINY_FONT))
                else:
                    text(draw, (4, 20), number[1], fill=turnColor)
                if number[2] == 'l':
                    text(draw, (24, 4), number[2], fill=turnColor, font=proportional(TINY_FONT))
                else:
                    text(draw, (21, 4), number[2], fill=turnColor)

        elif testlen == 4:
            with canvas(self.device) as draw:
                text(draw, (4, 4), number[0], fill=turnColor)
                if number[1] == 'l':
                    text(draw, (7, 20), number[1], fill=turnColor, font=proportional(TINY_FONT))
                else:
                    text(draw, (4, 20), number[1], fill=turnColor)
                if number[2] == 'l':
                    text(draw, (24, 4), number[2], fill=turnColor, font=proportional(TINY_FONT))
                else:
                    text(draw, (21, 4), number[2], fill=turnColor)
                if number[3] == 'l':
                    text(draw, (24, 20), number[3], fill=turnColor, font=proportional(TINY_FONT))
                else:
                    text(draw, (21, 20), number[3], fill=turnColor)

        elif testlen == 5:
            with canvas(self.device) as draw:
                text(draw, (4, 2), number[0], fill=turnColor)
                if number[1] == 'l':
                    text(draw, (7, 12), number[1], fill=turnColor, font=proportional(TINY_FONT))
                else:
                    text(draw, (4, 12), number[1], fill=turnColor)
                if number[2] == 'l':
                    text(draw, (7, 22), number[2], fill=turnColor, font=proportional(TINY_FONT))
                else:
                    text(draw, (4, 22), number[2], fill=turnColor)
                if number[3] == 'l':
                    text(draw, (24, 3), number[3], fill=turnColor, font=proportional(TINY_FONT))
                else:
                    text(draw, (21, 3), number[3], fill=turnColor)
                if number[4] == 'l':
                    text(draw, (24, 12), number[4], fill=turnColor, font=proportional(TINY_FONT))
                else:
                    text(draw, (21, 12), number[4], fill=turnColor)

        elif testlen == 6:
            with canvas(self.device) as draw:
                text(draw, (4, 2), number[0], fill=turnColor)
                if number[1] == "l":
                    text(draw, (7, 12), number[1], fill=turnColor, font=proportional(TINY_FONT))
                else:
                    text(draw, (4, 12), number[1], fill=turnColor)
                if number[2] == 'l':
                    text(draw, (7, 22), number[2], fill=turnColor, font=proportional(TINY_FONT))
                else:
                    text(draw, (4, 22), number[2], fill=turnColor)
                if number[3] == 'l':
                    text(draw, (24, 3), number[3], fill=turnColor, font=proportional(TINY_FONT))
                else:
                    text(draw, (21, 3), number[3], fill=turnColor)
                if number[4] == 'l':
                    text(draw, (24, 12), number[4], fill=turnColor, font=proportional(TINY_FONT))
                else:
                    text(draw, (21, 12), number[4], fill=turnColor)
                if number[5] == 'l':
                    text(draw, (24, 22), number[5], fill=turnColor, font=proportional(TINY_FONT))
                else:
                    text(draw, (21, 22), number[5], fill=turnColor)

    def SET_LED(self, number):
        self.SET_LED_set(number,1)
    def OFF_LED(self):
        self.SET_LED_set("000000",0)

if __name__ == "__main__":

    led = LED()
    led.SET_LED("7-1")
    time.sleep(3)
    led.OFF_LED()
    time.sleep(1)
    led.SET_LED("7-1")
    time.sleep(3)
    led.OFF_LED()
    led.device.cleanup()

