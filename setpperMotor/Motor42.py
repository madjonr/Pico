from A4988 import A4988
import rp2
from machine import Pin
import utime



SPEED_DELAY = 10
SPEED_TIME = 1000
INIT_SPEED = 100
A4988_STEPS = 16


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
    nop()               [10]
    jmp(x_dec, 'delay')
    mov(x, y)
    wrap()



class Motor42:
    """
    
    """        
    def __init__(self, sm_index, step, direction, ms1, ms2, ms3):
        self.step = step
        self.direction = direction
        a4988 = A4988(ms1, ms2, ms3)
        a4988.set_steps(A4988_STEPS)
        self.sm = rp2.StateMachine(sm_index, blink, freq=300000, set_base=step)
        self.sm.active(1)
        self.current_speed = INIT_SPEED




    def run(self, speed):
        self.sm.put(speed)
        self.current_speed = speed
        
    
    def stop(self):
        self.sm.active(0)
        

    def forward(self):
        self.direction.value(0)
        # print(self.direction.value())
    
    def back(self):
        self.direction.value(1)
        # print(self.direction.value())
        
    def speed_control(self, speed):
        step = abs(self.current_speed - speed)
        for i in range(step):
            self.current_speed = self.current_speed -1 if self.current_speed > speed else self.current_speed +1
            self.sm.put(self.current_speed)
            #if step <= 10:
                #delay = SPEED_DELAY
            #else:
                #delay = int(SPEED_TIME/step)
            utime.sleep_ms(SPEED_DELAY)
            #print(self.current_speed)



    
    
    
    

