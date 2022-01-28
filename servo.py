import utime
from machine import Pin, PWM


servo = PWM(Pin(16))
servo.freq(50)


while True:
    servo.duty_u16(1180)
    utime.sleep(2)
    servo.duty_u16(7500)
    utime.sleep(2)