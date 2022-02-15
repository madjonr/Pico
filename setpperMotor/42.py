from Motor42 import Motor42
from machine import Pin
import utime


motor_L_direction = Pin(0, Pin.OUT)
motor_L_step = Pin(1)
motor_L_s1 = Pin(3, Pin.OUT)
motor_L_s2 = Pin(4, Pin.OUT)
motor_L_s3 = Pin(5, Pin.OUT)

motor_R_direction = Pin(10, Pin.OUT)
motor_R_step = Pin(11)
motor_R_s1 = Pin(13, Pin.OUT)
motor_R_s2 = Pin(14, Pin.OUT)
motor_R_s3 = Pin(15, Pin.OUT)

motor_L = Motor42(0, motor_L_step, motor_L_direction, motor_L_s1, motor_L_s2, motor_L_s3)
motor_R = Motor42(1, motor_R_step, motor_R_direction, motor_R_s1, motor_R_s2, motor_R_s3)

motor_L.forward()
motor_L.run(3)

motor_R.forward()
motor_R.run(3)