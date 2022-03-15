
from machine import UART, Pin

blue = UART(0, tx=Pin(16), rx=Pin(17), baudrate=9600)
led = Pin(25, Pin.OUT)

msg = None


while True:
    if blue.any() > 0:
        msg = blue.read()
        print(msg)
        if b'\xff\x01\x01\x01\x02\x00\x01\x00' == msg:
            print('forward')
            led.value(1)  
        elif b'\xff\x01\x01\x01\x02\x00\x02\x00' == msg:
            print('back')
            led.value(1)
        elif b'\xff\x01\x01\x01\x02\x00\x04\x00' == msg:
            print('left')
            led.value(1)
        elif b'\xff\x01\x01\x01\x02\x00\x08\x00' == msg:
            print('right')
            led.value(1)
        elif b'\xff\x01\x01\x01\x02\x00\x00\x00' == msg:
            print('key up')
            led.value(0)
        else:
            print('other control')
        blue.write("recived {} \r\n".format(msg))
