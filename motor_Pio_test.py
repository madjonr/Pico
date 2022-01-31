import rp2
from machine import Pin, UART
import time


direction = Pin(16, Pin.OUT)
moto_ms1 = Pin(6, Pin.OUT)
moto_ms2 = Pin(7, Pin.OUT)
moto_ms3 = Pin(8, Pin.OUT)

moto_ms1.high()
moto_ms2.high()
moto_ms3.high()


blue = UART(1, tx=Pin(4), rx=Pin(5), baudrate=9600)
msg = 'null'

speed = 10
direction.value(1)

@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW, out_shiftdir=rp2.PIO.SHIFT_RIGHT, autopull=True)
def blink():
    #out(x, 32)
    wrap_target()
    mov(x, osr)
    mov(y, x)
    set(pins, 1)
    label('high_loop')
    nop()                     
    jmp(x_dec, 'high_loop')   

    set(pins, 0)               
    label('low_loop')
    nop()                     
    jmp(y_dec, 'low_loop')                  
    wrap()
    
    
sm = rp2.StateMachine(0, blink, freq=200000, set_base=Pin(17))
sm.active(1)



sm.put(10)
time.sleep(3)
sm.put(2)
time.sleep(3)
sm.put(3)
time.sleep(3)
sm.put(4)



#for i in range(100):
   #sm.restart()
#   sm.put(i)
#   time.sleep(1)





