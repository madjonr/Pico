from machine import Pin
import utime


motor1a = Pin(16, Pin.OUT)
motor1b = Pin(17, Pin.OUT)


def forward():
    motor1a.high()
    motor1b.low()
    

def backward():
    motor1a.low()
    motor1b.high()
    
    
def stop():
    motor1a.low()
    motor1b.low()
    
    
def test():
    forward()
    utime.sleep(2)
    stop()
    backward()
    utime.sleep(2)
    stop()
    
    
test()