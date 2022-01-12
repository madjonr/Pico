
from sys import platform
from machine import Pin, freq, I2C
import utime
import gc
from sh1106 import SH1106_I2C
from nec import NEC_8, NEC_16
from print_error import print_error  



i2c = I2C(0)
oled = SH1106_I2C(128, 64, i2c)
oled.rotate(True)


def callback(data, addr, ctrl):
    if data < 0:  # NEC protocol sends repeat codes.
        print('Repeat code.')
    else:
        print('Data {:02x} Addr {:04x} Ctrl {:02x}'.format(data, addr, ctrl))
    oled.fill(0)
    oled.text("pressed: {:02x}".format(data), 10, 10)
    oled.show()
    
    
def run(proto=0):
    ir = NEC_8(Pin(11, Pin.IN), callback)  # Instantiate receiver
    ir.error_function(print_error)  # Show debug information
    #ir.verbose = True
    # A real application would do something here...
    try:
        while True:
            print('running')
            utime.sleep(5)
            gc.collect()
    except KeyboardInterrupt:
        ir.close()


run()


