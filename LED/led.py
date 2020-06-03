
import re
import time
import argparse

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT


def demo(number):
    number = number.replace('-', 'l')
    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial, width=32, height=32, block_orientation=-90, rotate=1)
    testlen = len(number)

    if testlen == 1:
        with canvas(device) as draw:
            text(draw, (4, 4), number[0], fill="white")

    elif testlen == 2:
        with canvas(device) as draw:
            text(draw, (4, 4), number[0], fill="white")
            text(draw, (4, 20), number[1], fill="white")

    elif testlen == 3:
        with canvas(device) as draw:
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
        with canvas(device) as draw:
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
        with canvas(device) as draw:
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
        with canvas(device) as draw:
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

    print(number)
    time.sleep(10)
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='matrix_demo arguments',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--cascaded', '-n', type=int, default=1, help='Number of cascaded MAX7219 LED matrices')
    parser.add_argument('--block-orientation', type=int, default=0, choices=[0, 90, -90],
                        help='Corrects block orientation when wired vertically')
    parser.add_argument('--rotate', type=int, default=0, choices=[0, 1, 2, 3],
                        help='Rotate display 0=0, 1=90, 2=180, 3=270')
    parser.add_argument('--reverse-order', type=bool, default=False, help='Set to true if blocks are in reverse order')

    args = parser.parse_args()

    try:
        demo("4000-1")
    except KeyboardInterrupt:
        pass
