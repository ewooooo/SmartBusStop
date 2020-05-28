import re
import time
import argparse

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT

class led():

def demo(n, block_orientation, rotate, inreverse):
    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial,width=32,height=32,block_orientation=-90,rotate=2)

    time.sleep(4)
    msg="abcd"
    with canvas(device) as draw:
       text(draw, (3, 4), msg[0], fill="white")
       text(draw, (3, 20), msg[1], fill="white")
       text(draw, (11, 4), msg[2], fill="white")
       text(draw, (11, 20), msg[3], fill="white")
    print(msg1)
    time.sleep(4)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='matrix_demo arguments',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--cascaded', '-n', type=int, default=1, help='Number of cascaded MAX7219 LED matrices')                                                               
    parser.add_argument('--block-orientation', type=int, default=0, choices=[0, 90, -90], help='Corrects block orientation when wired vertically')
    parser.add_argument('--rotate', type=int, default=0, choices=[0, 1, 2, 3], help='Rotate display 0=0, 1=90, 2=180, 3=270')
    parser.add_argument('--reverse-order', type=bool, default=False, help='Set to true if blocks are in reverse order')

    args = parser.parse_args()

    try:
        demo(args.cascaded, args.block_orientation, args.rotate, args.reverse_order)
    except KeyboardInterrupt:
        pass
