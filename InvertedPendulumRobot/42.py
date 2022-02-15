from machine import Pin, I2C
import utime
from imu import MPU6050
from Motor42 import Motor
from PID import PID


BALANCE_ANGLE = 0.04

i2c = I2C(1, sda=Pin(26), scl=Pin(27), freq=400000)
imu = MPU6050(i2c)


motor = Motor()

#motor.start()
#motor.speed_control(10)


pid = PID(0.1, 0.01, 0.01, setpoint=BALANCE_ANGLE)
pid.output_limits = (-0.3, 0.3)


while True:
    ax=round(imu.accel.x,2)
    #ay=round(imu.accel.y,2)
    #az=round(imu.accel.z,2)
    #gx=round(imu.gyro.x)
    #gy=round(imu.gyro.y)
    #gz=round(imu.gyro.z)
    #tem=round(imu.temperature,2)
    # print(ax,"\t",ay,"\t",az,"\t",gx,"\t",gy,"\t",gz,"\t",tem,"        ",end="\r")
    # print('ax:{:04}\t ay:{:04}\t az:{:04}\t gx:{:04}\t gy:{:04}\t gz:{:04}\r'.format(ax, ay, az, gx, gy, gz))
    
    
    angle = pid(ax)
    #print("ax:{}  angle:{}".format(ax, angle))
    print(angle)
    if angle > 0:
        motor.forward()
        motor.speed_control(motor.current_speed - int(angle*100))
    elif angle < -0:
        motor.back()
        motor.speed_control(motor.current_speed + int(angle*100))
    else:
        motor.speed_control(30)
    
    utime.sleep_ms(10)
    
    
    
    



