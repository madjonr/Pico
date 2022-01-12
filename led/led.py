from machine import Pin, PWM, ADC
import time

adc = ADC(Pin(28))
pwm1 = PWM(Pin(2))
pwm2 = PWM(Pin(3))
pwm1.freq(1000)
pwm2.freq(1000)

while True:
    pwm1.duty_u16(adc.read_u16())
    print(adc.read_u16())
    pwm2.duty_u16(65535-adc.read_u16())
    time.sleep(0.001)
