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
    label('setXfromOSR')
    out(x, 32)
    mov(y, x)
    wrap_target()
    jmp(not_osre, 'setXfromOSR')
    set(pins, 1)
    set(pins, 0)
    label('delay')
    nop()
    jmp(not_x, 'setXfromY')
    jmp(x_dec, 'delay')
    label('setXfromY')
    mov(x, y)
    
    
sm = rp2.StateMachine(0, blink, freq=200000, set_base=Pin(17))
sm.active(1)



sm.put(1)
time.sleep(1)
sm.put(2)
time.sleep(1)
sm.put(3)
time.sleep(1)
sm.put(4)
time.sleep(1)
sm.put(5)
time.sleep(1)
sm.put(6)
time.sleep(1)
sm.put(7)
time.sleep(1)
sm.put(8)




#for i in range(100):
   #sm.restart()
#   sm.put(i)
#   time.sleep(1)





