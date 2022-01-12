from machine import UART, Pin

#blue = UART(1,9600)
blue = UART(1, tx=Pin(4), rx=Pin(5), baudrate=9600)
led = Pin(25, Pin.OUT)
red = Pin(15, Pin.OUT)
green = Pin(14, Pin.OUT)

while True:
    if blue.any() > 0:
        msg = blue.read()
        print(msg)
        if b'red' == msg:
            led.value(1)
            red.value(1)
            green.value(0)
            blue.write("red on green off\r\n")
        elif "green" in msg:
            led.value(0)
            red.value(0)
            green.value(1)
            blue.write("red off green on\r\n")
        else:
            blue.write("all off\r\n")
            red.value(0)
            green.value(0)