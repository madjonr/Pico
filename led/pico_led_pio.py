import rp2, time
from machine import Pin
@rp2.asm_pio(out_init=rp2.PIO.OUT_LOW,
             out_shiftdir=rp2.PIO.SHIFT_RIGHT,
             autopull=True, pull_thresh=1)
def blink():
    wrap_target()
    out(pins, 1)
    wrap()
sm = rp2.StateMachine(0, blink, out_base=Pin(25))
sm.active(1)
while True:
    sm.put(1)
    time.sleep(1)
    sm.put(2)
    time.sleep(0)