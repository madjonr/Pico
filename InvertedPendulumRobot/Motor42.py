from A4988 import A4988
import rp2
from machine import Pin
import utime




A4988_STEPS = 16
SPEED_INIT = 60
SPEED_DELAY = 40
SPEED_TIME = 1000
current_speed_L = 100
current_speed_R = 100
SPEED_MIN = 1
SPEED_MAX = 100


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




@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW, out_shiftdir=rp2.PIO.SHIFT_RIGHT, autopull=True)
def blink():
    label('setXfromOSR')
    out(x, 32)
    mov(y, x)
    wrap_target()
    jmp(not_osre, 'setXfromOSR')
    set(pins, 1)        
    set(pins, 0)        
    label('delay')
    nop()               [15]
    nop()               [15]
    jmp(x_dec, 'delay')
    mov(x, y)
    wrap()



class Motor:
    """
    
    """        
    def __init__(self):
        a4988_L = A4988(motor_L_s1, motor_L_s2, motor_L_s3)
        a4988_L.set_steps(A4988_STEPS)
        a4988_R = A4988(motor_R_s1, motor_R_s2, motor_R_s3)
        a4988_R.set_steps(A4988_STEPS)
        self.sm_L = rp2.StateMachine(0, blink, freq=1000000, set_base=motor_L_step)
        self.sm_L.active(1)
        self.sm_R = rp2.StateMachine(1, blink, freq=1000000, set_base=motor_R_step)
        self.sm_R.active(1)
        
        self.current_speed = SPEED_INIT




    def start(self, speed=SPEED_INIT):
        self.sm_L.put(speed)
        self.sm_R.put(speed)
        
    
    def close(self):
        self.sm_L.active(0)
        self.sm_R.active(0)
        
    def stop(self):
        speed_control(0)
        

    def forward(self):
        motor_L_direction.value(0)
        motor_R_direction.value(0)
        # print(self.direction.value())
    
    def back(self):
        motor_L_direction.value(1)
        motor_R_direction.value(1)
        # print(self.direction.value())
        

    def speed_limits(self, speed):
        if speed <= SPEED_MIN:
            return SPEED_MIN
        elif speed >= SPEED_MAX:
            return SPEED_MAX
        else:
            return speed
            
    def speed_control(self, speed):
        speed = self.speed_limits(speed)
        self.sm_L.put(speed)
        self.sm_R.put(speed)
        # self.current_speed = speed
        
        
    def trun_R(self):
        self.sm_R.put(0)
        
        
    def trun_R(self):
        self.sm_L.put(0)

        




    
    
    
    
