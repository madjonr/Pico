from machine import Pin, I2C, freq, UART
import utime
from imu import MPU6050
from motor import Motor
from PID import PID
from angleFilter import Filter
from BalanceCarPID import carPID



class InvertedPendulumRobot:
    
    def __init__(self):
        self.balence_angle = 1.85
        self.velocity_point = 0
        self.motor = Motor()
        self.filter = Filter()
        self.maxpitch = 30

    
    def start(self):
        self.motor.start()
        
        
    def stop(self):
        self.motor.stop()
        
        
    def forward(self, pid):
        pid.setpoint = self.balence_angle + self.maxpitch*0.05

    def back(self, pid):
        pid.setpoint = self.balence_angle - self.maxpitch*0.05
    
    def turn_left(self):
        self.motor.turn_left()
    
    def left_forward(self):
        self.motor.left_forward()
        
    def turn_right(self):
        self.motor.turn_right()

    def right_forward(self):
        self.motor.right_forward()
        
    def stand(self, pid):
        pid.setpoint = self.balence_angle
    

    def update(self, speed):
        self.motor.speed_control(speed)
    
    
        
if __name__ == '__main__':
    blue = UART(0, tx=Pin(16), rx=Pin(17), baudrate=9600)
    led = Pin(25, Pin.OUT)

    i2c = I2C(1, sda=Pin(26), scl=Pin(27), freq=400000)
    imu = MPU6050(i2c)
    
    robot = InvertedPendulumRobot()
    #stand_pid = carPID(80.0, 1.0, 0.8, setpoint=robot.balence_angle)
    stand_pid = PID(80.0, 1.0, 0.1, setpoint=robot.balence_angle)
    stand_pid.output_limits = (-1000, 1000)
    
    
    velocity_pid = PID(10, 0.1, 0.1, setpoint=robot.velocity_point)
    velocity_pid.output_limits = (-100, 100)
    
    keyPressed = ''

    robot.start()    
    #robot.motor.set_speed(8010)


    while True:
        #ax=round(imu.accel.x,2)
        #ay=round(imu.accel.y,2)
        #az=round(imu.accel.z,2)
        #gx=round(imu.gyro.x)
        #gy=round(imu.gyro.y)
        #gz=round(imu.gyro.z)
        #tem=round(imu.temperature,2)
        #print(ax,"\t",ay,"\t",az,"\t",gx,"\t",gy,"\t",gz,"\t",tem,"        ",end="\r")
        #print('ax:{:04}\t ay:{:04}\t az:{:04}\t gx:{:04}\t gy:{:04}\t gz:{:04}\r'.format(ax, ay, az, gx, gy, gz))

        angle = robot.filter.complementary(imu)
        if angle >= robot.maxpitch or angle <= -robot.maxpitch:
            print("motor stop!!")
            robot.motor.stop()
            break

        speed = stand_pid(angle, imu.gyro.x)
        speed = robot.filter.filter_speed(speed, 0.5)
        print('angle:{}  speed:{}'.format(angle, speed))
        robot.update(speed)
        
        if blue.any() > 0:
            msg = blue.read()
            print(msg)
            if b'\xff\x01\x01\x01\x02\x00\x01\x00' == msg:
                robot.forward(pid)
                print('forward')
                led.value(1)  
            elif b'\xff\x01\x01\x01\x02\x00\x02\x00' == msg:
                robot.back(pid)
                print('back')
                led.value(1)
            elif b'\xff\x01\x01\x01\x02\x00\x04\x00' == msg:
                keyPressed = 'left'
                robot.turn_left()
                print('left')
                led.value(1)
            elif b'\xff\x01\x01\x01\x02\x00\x08\x00' == msg:
                keyPressed = 'right'
                robot.turn_right()
                print('right')
                led.value(1)
            elif b'\xff\x01\x01\x01\x02\x00\x00\x00' == msg:
                robot.stand(pid)
                if keyPressed == 'left':
                    robot.left_forward()
                if keyPressed == 'right':
                    robot.right_forward()                    
                print('key up')
                led.value(0)
            else:
                print('other control')
            blue.write("recived {} \r\n".format(msg))
        #utime.sleep_ms(10)


        
    
    
    
    






