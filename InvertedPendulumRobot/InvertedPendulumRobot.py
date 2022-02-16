from machine import Pin, I2C, freq
import utime
from imu import MPU6050
from Motor42 import Motor
from PID import PID
from math import pow


#freq(133000000)

class InvertedPendulumRobot:
    
    def __init__(self):
        self.balence_angle = 0.04
        self.motor = Motor()

        
        

    def update(self, angle):
        if angle > 0:
            self.motor.forward()
            self.motor.speed_control(self.motor.current_speed - int(angle*70))
        elif angle < 0:
            self.motor.back()
            self.motor.speed_control(self.motor.current_speed + int(angle*70))
        else:
            self.motor.speed_control(0)

    def balance(self, angle, gyro):
        '''
        直立PD环
        '''
        bias = 0
        balance_KP = 20
        balance_KD = 0.01
        balance = 0
        bias = angle - self.balence_angle
        balance = balance_KP * bias + balance_KD * gyro
        return balance 

if __name__ == '__main__':
    i2c = I2C(1, sda=Pin(26), scl=Pin(27), freq=400000)
    imu = MPU6050(i2c)
    
    robot = InvertedPendulumRobot()
    pid = PID(0.1, 0.03, 0.02, setpoint=robot.balence_angle)
    pid.output_limits = (-0.6, 0.6)
    



    while True:
        ax=round(imu.accel.x,2)
        #ay=round(imu.accel.y,2)
        #az=round(imu.accel.z,2)
        #gx=round(imu.gyro.x)
        #gy=round(imu.gyro.y)
        #gz=round(imu.gyro.z)
        #tem=round(imu.temperature,2)
        # print(ax,"\t",ay,"\t",az,"\t",gx,"\t",gy,"\t",gz,"\t",tem,"        ",end="\r")
        #print('ax:{:04}\t ay:{:04}\t az:{:04}\t gx:{:04}\t gy:{:04}\t gz:{:04}\r'.format(ax, ay, az, gx, gy, gz))
        

        
        angle = pid(ax)
        #print("ax:{}  angle:{}".format(ax, angle))
        #print(ax)
        #print(gy)
        #angle = robot.balance(ax, gy)
        print(angle)
        robot.update(angle)
        #utime.sleep_ms(10)

        
    
    
    
    



