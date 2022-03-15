
from math import atan, sqrt, degrees, sin, cos, tan, isnan
import utime


class Filter(object):
    """
    滤波
    """
    
    def __init__(self):
        self.last_angle = 0
        self.last_speed = 0
        self.last_gyro_angle = None
        
        self.__angle   = float('nan')
        
        self.__alpha = 0.05
        self.__time  = utime.ticks_us()
        self.__delta = utime.ticks_diff(utime.ticks_us(), self.__time)/1000000
    
        
        
    def calculate_angle_acceleration(self, ax, ay, az):
        """
        通过加速度计算翻滚角 roll
        加速度转换成偏角乘*180/pi就是角度，不乘就是欧拉角
        """
        roll = int(degrees(atan2(ay/sqrt(ax**2+az**2+1e-16))))
        pitch = int(degrees(atan(-ax/sqrt(ay**2+az**2+1e-16))))
        return (roll, pitch)


    def calculate_angle_gyro(self, gx, gy, gz):
        """
        通过陀螺仪数据计算偏转角度
        gx: roll 翻滚角速度
        gy: pitch 俯仰角速度
        gz: yaw 偏航角速度
        """
        if isnan(self.__angle):
            self.__angle = angle          
        self.__delta = utime.ticks_diff(utime.ticks_us(), self.__time)/1000000
        self.last_gyro_angle[0] += gx * self.__delta
        self.last_gyro_angle[1] += gy * self.__delta
        self.last_gyro_angle[2] += gz * self.__delta
        self.last_gyro_angle = (self.angle_x, self.angle_y, self.angle_z)
        return self.last_gyro_angle
    
    
    def complementary(self, imu):
        """
        互补滤波
        """
        angle = round(degrees(atan(round(imu.accel.y,2)/sqrt(round(imu.accel.x,2)**2+round(imu.accel.z,2)**2))),2)
        if isnan(self.__angle):
            self.__angle = angle          
        self.__delta = utime.ticks_diff(utime.ticks_us(), self.__time)/1000000
        self.__time  = utime.ticks_us()
        self.__angle = (1-self.__alpha) * (self.__angle + imu.gyro.x * self.__delta) + self.__alpha * angle
        return self.__angle
        
    
    def kalman(self):
        return o


    def filter_angle(self, curent_angle):
        """
        一价滤波器，减少抖动
        """
        self.last_angle *= 0.8
        curent_angle = curent_angle*0.2 + self.last_angle
        self.last_angle = curent_angle
        return curent_angle
        
        
    def filter_speed(self, curent_speed, alpha):
        """
        一价滤波器，减少抖动
        """
        curent_speed = curent_speed*alpha + self.last_speed*(1-alpha)
        self.last_speed = curent_speed
        return curent_speed



#__> Kalman Filter
class Filters(object):
    def __init__(self, R:float, Q:float, alpha:float) -> None:
        self.__cov = float('nan')
        self.__x   = float('nan')
        self.__c   = float('nan')
        self.__A, self.__B, self.__C = 1, 0, 1
        self.__R, self.__Q = R, Q
        
        self.__alpha = alpha
        self.__time  = utime.ticks_us()
        self.__delta = utime.ticks_diff(utime.ticks_us(), self.__time)/1000000

    def kalman(self, angle:float) -> float:
        u = 0
        if math.isnan(self.__x):
            self.__x   = (1 / self.__C) * angle
            self.__cov = (1 / self.__C) * self.__Q * (1 / self.__C)
        else:
            px         = (self.__A * self.__x) + (self.__B * u)
            pc         = ((self.__A * self.__cov) * self.__A) + self.__R
            K          = pc * self.__C * (1 / ((self.__C * pc * self.__C) + self.__Q))
            self.__x   = px + K * (angle - (self.__C * px))
            self.__cov = pc - (K * self.__C * pc)

        return self.__x
        
    def complementary(self, rate:float, angle:float) -> float:
        if math.isnan(self.__c):
            self.__c = angle
            
        self.__delta = utime.ticks_diff(utime.ticks_us(), self.__time)/1000000
        self.__time  = utime.ticks_us()
        self.__c     = (1-self.__alpha) * (self.__c + rate * self.__delta) + self.__alpha * angle
        return self.__c

    
    