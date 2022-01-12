from machine import I2C
from sh1106 import SH1106_I2C
import time

i2c = I2C(0)
oled = SH1106_I2C(128, 64, i2c)

oled.rotate(True)
#oled.fill(0)
#oled.text("hello teanur", 10, 10)
#oled.text("go play wow", 10, 20)
#oled.show()

counter = 0

while True:
    oled.fill(0)
    oled.text("hello teanur", 10, 10)
    oled.text("go play wow", 10, 20)
    oled.text("hello {}".format(counter), 10, 40)
    oled.show()
    counter += 1
    time.sleep(0.5)