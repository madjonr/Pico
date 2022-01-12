from machine import Pin, PWM, ADC
import utime

pwm1 = PWM(Pin(13))
motor1b = Pin(12, Pin.OUT)
adc = ADC(Pin(26))


pwm1.freq(10000)


def motorRun(speed, clolckwise_pwm=None, anti_clockwise_pin=None):
    pwm1.duty_u16(adc.read_u16())
    motor1b.low()
    #pwm2.duty_u16(100)
    #print("ddd")
    
#motorRun(50)


while True:
    pwm1.duty_u16(adc.read_u16())
    motor1b.low()