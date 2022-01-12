from machine import Pin, ADC, PWM
import time

adc = ADC(Pin(26))
pwm = PWM(Pin(15))

pwm.freq(1000)

while True:
    print(adc.read_u16())
    #for i in range(65025):
        #pwm.duty_u16(i)
        #time.sleep(0.005)
    time.sleep(1)