from A4988 import A4988
import rp2
from machine import Pin, PWM
import utime




A4988_STEPS = 16
FREQ_RANGE = (15, 9015)
SPEED_RANGE= (0, 1000)
DUTY_CYCLE = 2**16//2 + 255

motor_L_direction = Pin(0, Pin.OUT)
motor_L_step = Pin(1, Pin.OUT)
motor_L_s3 = Pin(3, Pin.OUT)
motor_L_s2 = Pin(4, Pin.OUT)
motor_L_s1 = Pin(5, Pin.OUT)

motor_R_direction = Pin(10, Pin.OUT)
motor_R_step = Pin(11, Pin.OUT)
motor_R_s3 = Pin(13, Pin.OUT)
motor_R_s2 = Pin(14, Pin.OUT)
motor_R_s1 = Pin(15, Pin.OUT)






class Motor:
    """
    
    """        
    def __init__(self):
        _a4988_L = A4988(motor_L_s1, motor_L_s2, motor_L_s3)
        _a4988_L.set_steps(A4988_STEPS)
        _a4988_R = A4988(motor_R_s1, motor_R_s2, motor_R_s3)
        _a4988_R.set_steps(A4988_STEPS)
        self.pwm_L = PWM(motor_L_step)
        self.pwm_R = PWM(motor_R_step)
        speed_range = (SPEED_RANGE[1] - SPEED_RANGE[0]) /2 
        self.freq_speed = (FREQ_RANGE[1] - FREQ_RANGE[0]) / speed_range
        self.speed_L = 0
        self.speed_R = 0
        self.direction = ''


    def start(self):
        self.pwm_L.duty_u16(DUTY_CYCLE)
        self.pwm_R.duty_u16(DUTY_CYCLE)
        self.pwm_L.freq(FREQ_RANGE[0])
        self.pwm_R.freq(FREQ_RANGE[0])
        
    
        
    def stop(self):
        self.pwm_L.deinit()
        self.pwm_R.deinit()
        

    def forward(self):
        motor_L_direction.value(0)
        motor_R_direction.value(0)
        
    
    def back(self):
        motor_L_direction.value(1)
        motor_R_direction.value(1)
        
        
    def turn_right(self):
        self.direction = 'right'
        #speed = self.freq_limits(int(abs(self.curent_speed+10) * self.freq_speed))
        #self.speed_L = speed
        #self.pwm_L.freq(speed)
    def right_forward(self):
        self.direction = 'right_forward'
        #speed = self.freq_limits(int(abs(self.curent_speed-10) * self.freq_speed))
        #self.speed_L = speed
        
        
    def turn_left(self):
        self.direction = 'left'
        #speed = self.freq_limits(int(abs(self.curent_speed+10) * self.freq_speed))
        #self.speed_R = speed
        #self.pwm_R.freq(speed)
        
    def left_forward(self):
        self.direction = 'left_forward'
        #speed = self.freq_limits(int(abs(self.curent_speed-10) * self.freq_speed))
        #self.speed_R = speed


    def speed_limits(self, speed):
        speed_min, speed_max = SPEED_RANGE
        if speed < speed_min:
            return speed_min
        elif speed > speed_max:
            return speed_max
        else:
            return speed
        
    
    def speed_to_freq(self, speed):
        return int(max(min(FREQ_RANGE[1], (speed - SPEED_RANGE[0]) * (FREQ_RANGE[1] - FREQ_RANGE[0]) // (SPEED_RANGE[1] - SPEED_RANGE[0]) + FREQ_RANGE[0]), FREQ_RANGE[0]))
    
            
    def speed_control(self, pid_output):
        speed = self.speed_to_freq(abs(pid_output))
        self.speed_L = speed
        self.speed_R = speed
        if pid_output < 0:
            self.forward()
        else:
            self.back()
        self.pwm_L.freq(self.speed_L)
        self.pwm_R.freq(self.speed_R)
        
        
        
    def set_speed(self, speed):
        self.pwm_L.freq(speed)
        self.pwm_R.freq(speed)


        




    
    
    
    



