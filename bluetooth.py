from machine import UART, Pin, I2C
from sh1106 import SH1106_I2C
import utime


#blue = UART(1,9600)
blue = UART(1, tx=Pin(8), rx=Pin(9), baudrate=9600)
led = Pin(25, Pin.OUT)

i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled = SH1106_I2C(128, 64, i2c)

oled.rotate(True)

msg = 'null'

while True:
    oled.fill(0)
    oled.text("bluetooth HC-08", 10, 10)
    oled.text("test data", 10, 20)
    if blue.any() > 0:
        msg = blue.read()
        print(msg)
        if b'on' == msg:
            led.value(1)
        elif "off" in msg:
            led.value(0)
        else:
            led.value(0)
        blue.write("recived {} \r\n".format(msg))
    oled.text("data {}".format(str(msg)), 2, 40)
    oled.show()
    #utime.sleep(1)
