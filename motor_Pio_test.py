import rp2
from machine import Pin
import gc
from nec import NEC_8, NEC_16
from print_error import print_error  


direction = Pin(16, Pin.OUT)
moto_ms1 = Pin(6, Pin.OUT)
moto_ms2 = Pin(7, Pin.OUT)
moto_ms3 = Pin(8, Pin.OUT)

moto_ms1.high()
moto_ms2.high()
moto_ms3.high()


speed = 10
direction.value(0)

@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW, out_shiftdir=rp2.PIO.SHIFT_RIGHT, autopull=True)
def blink():
    mov(x, osr)
    #mov(y, x)
    set(pins, 1)              [1]        
    label('loop')
    nop()                     [1]                  
    jmp(x_dec, 'loop')    
    set(pins, 0)              [1]  
    #label('low_loop')
    #nop()                     
    #jmp(y_dec, 'low_loop')
    
    
sm = rp2.StateMachine(0, blink, freq=200000, set_base=Pin(17))
sm.active(1)



while True:
    sm.put(speed)