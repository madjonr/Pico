import rp2
from machine import Pin
@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def blink():
    wrap_target()
    
    set(pins, 1)
    set(x, 24)                [23]
    label('high_loop')
    nop()                     [19]
    nop()                     [19]
    nop()                     [19]
    jmp(x_dec, 'high_loop')   [18]
    
    set(pins, 0)
    set(x, 24)                [23]
    label('low_loop')
    nop()                     [19]
    nop()                     [19]
    nop()                     [19]
    jmp(x_dec, 'low_loop')    [18]
    
    wrap()
sm = rp2.StateMachine(0, blink, freq=2000, set_base=Pin(25))
sm.active(1)