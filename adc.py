from machine import Pin, ADC, PWM
import time

adc = ADC(Pin(28))
pwm = PWM(Pin(5))

pwm.freq(1000)

while True:
    print(adc.read_u16())
    pwm.duty_u16(adc.read_u16())
    time.sleep(0.1)
