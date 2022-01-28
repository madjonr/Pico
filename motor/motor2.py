from machine import Pin, PWM, ADC
import utime

pwm1 = PWM(Pin(17))
motor1b = Pin(16, Pin.OUT)
adc = ADC(Pin(28))


pwm1.freq(10000)


#def motorRun(speed=50, clolckwise_pwm=None, anti_clockwise_pin=None):
    #clolckwise_pwm.duty_u16(int(65535*speed/100))
    #anti_clockwise_pin.low()
    #pwm1.duty_u16(100)
    #print("start")
    
#motorRun(15, pwm1, motor1b)


while True:
    #pwm1.duty_u16(adc.read_u16())
    #motor1b.low()
    print(adc.read_u16())
    #print("speed:{}".format(adc.read_u16()/65535*100))