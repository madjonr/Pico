from machine import Pin, PWM
import utime


motor_L_direction = Pin(10, Pin.OUT)
motor_L_s1 = Pin(13, Pin.OUT)
motor_L_s2 = Pin(14, Pin.OUT)
motor_L_s3 = Pin(15, Pin.OUT)
motor_L_direction.value(0)
motor_L_s1.high()
motor_L_s2.high()
motor_L_s3.high()

pwm0 = PWM(Pin(11, Pin.OUT))      # create PWM object from a pin
pwm0.duty_u16(2**16//2 + 255)      # set duty cycle, range 0-65535
pwm0.freq(10)         # set frequency
utime.sleep(3)
#pwm0.deinit()
pwm0.freq(10000)

#pwm=PWM(Pin(1), freq=300000, duty_u16=2**16//2 + 255)