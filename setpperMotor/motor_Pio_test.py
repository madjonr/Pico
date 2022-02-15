import rp2
from machine import Pin
import utime


direction = Pin(0, Pin.OUT)
moto_ms1 = Pin(3, Pin.OUT)
moto_ms2 = Pin(4, Pin.OUT)
moto_ms3 = Pin(5, Pin.OUT)

moto_ms1.high()
moto_ms2.high()
moto_ms3.high()



direction.value(0)

@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW, out_shiftdir=rp2.PIO.SHIFT_RIGHT, autopull=True)
def blink():
    label('setXfromOSR')
    out(x, 32)
    mov(y, x)
    wrap_target()
    jmp(not_osre, 'setXfromOSR')
    set(pins, 1)        [1]
    set(pins, 0)        [1]
    label('delay')
    nop()               [31]
    jmp(x_dec, 'delay')
    mov(x, y)
    wrap()
    
sm = rp2.StateMachine(0, blink, freq=300000, set_base=Pin(1))
sm.active(1)



#sm.put(5)





for i in range(100):
   #sm.restart()
   sm.put(i)
   utime.sleep_ms(200)





