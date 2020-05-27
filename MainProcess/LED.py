import re
import time
import argparse

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT


def demo():
    # create matrix device
    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial,width=32,height=24,block_orientation=-90,rotate=3)
    
    # 8,32  finish
    # start demo
    msg = "hello"
    print(msg)  #start on msg
    show_message(device, msg, fill="white", font=proportional(LCD_FONT),scroll_delay=0.1)
    #time.sleep(1)
    #show_message(device2, msg, fill="white", font=proportional(LCD_FONT),scroll_delay=0.1)
    #time.sleep(1)
    #show_message(device3, msg, fill="white", font=proportional(LCD_FONT),scroll_delay=0.1)
    #time.sleep(1)
    #show_message(device4, msg, fill="white", font=proportional(LCD_FONT),scroll_delay=0.1)
    time.sleep(1)

    #test
    time.sleep(1)
    msg1="a"
    with canvas(device) as draw:
        draw.rectangle(device.bounding_box, outline="white", fill="black")
        text(draw, (4,4), msg1, fill="white",font=proportional(CP437_FONT))
        text(draw, (4,18), "1", fill="white")
        text(draw, (20,3), "e", fill="white")
        text(draw, (20,11), "5", fill="white")
        
    print(msg1)
    time.sleep(4)

  #  time.sleep(1)
   # for _ in range(5):
    #    for intensity in range(16):
     #       device.contrast(intensity * 16)
      #      time.sleep(0.1)

   # device.contrast(0x80)
   # time.sleep(1)

if __name__ == "__main__":
  
    try:
        demo()
    except KeyboardInterrupt:
        pass
