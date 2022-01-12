from machine import I2C, Pin
from sh1106 import SH1106_I2C
import time

#i2c = I2C(0) 根据raspberry pi Pico的设定，id只有0和1这2个值，I2C(0)是默认指5和4脚
# 通过i2c.scan() 扫描得出0x30的值配置到sh1106.py文件初始化SH1106_I2C的addr=0x3c中
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
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