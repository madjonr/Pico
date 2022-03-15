from machine import Pin, I2C, freq
import utime
from imu import MPU6050
from Motor42 import Motor
from PID import PID
#from BalanceCarPID import PID
from math import atan, pi, sqrt


#freq(133000000)

class InvertedPendulumRobot:
    
    def __init__(self):
        self.balence_angle = 0
        self.motor = Motor()
        self.active = False

    
    def start(self):
        self.active = True
        self.motor.start()
        
    def stop(self):
        self.active = False
        self.motor.stop()
        

    def update(self, speed):
        speed = int(speed)
        self.motor.speed_control(speed)

    def balance(self, angle, gyro):
        '''
        直立PD环
        '''
        bias = 0
        balance_KP = 0.4
        balance_KD = -0.004
        balance = 0
        bias = angle - self.balence_angle
        balance = balance_KP * bias + balance_KD * gyro
        return balance
    
    
    def acceleration_limits(self, acceleration):
        if acceleration < -1:
            return -1
        elif acceleration > 1:
            return 1
        else:
            return acceleration
        
        
    def angle(self, ax, ay, az):
        return int(atan(ax/sqrt((pow(ay,2)+pow(az,2))))*180/pi)
    

if __name__ == '__main__':
    i2c = I2C(1, sda=Pin(26), scl=Pin(27), freq=400000)
    imu = MPU6050(i2c)
    
    robot = InvertedPendulumRobot()
    pid = PID(0.1, 0.01, 0.001, setpoint=robot.balence_angle)
    pid.output_limits = (-29, 29)
    
    robot.start()

    #robot.motor.set_speed(1)


    while True:
        ax=round(imu.accel.x,2)
        ay=round(imu.accel.y,2)
        az=round(imu.accel.z,2)
        #gx=round(imu.gyro.x)
        gy=round(imu.gyro.y)
        #gz=round(imu.gyro.z)
        #tem=round(imu.temperature,2)
        # print(ax,"\t",ay,"\t",az,"\t",gx,"\t",gy,"\t",gz,"\t",tem,"        ",end="\r")
        # print('ax:{:04}\t ay:{:04}\t az:{:04}\t gx:{:04}\t gy:{:04}\t gz:{:04}\r'.format(ax, ay, az, gx, gy, gz))
        angle = robot.angle(ax, ay, az)
        #speed = pid(angle)
        speed = robot.balance(angle, gy)
        print('angle:{}  speed:{}\t\r'.format(angle, speed))
        robot.update(speed)
        utime.sleep_ms(10)


        
    
    
    
    



