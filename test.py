
import rp2, time
from machine import Pin
import gc, utime
from nec import NEC_8, NEC_16
from print_error import print_error


@rp2.asm_pio(out_init=rp2.PIO.OUT_LOW,
             out_shiftdir=rp2.PIO.SHIFT_RIGHT,
             autopull=True)
def blink():
    out(x, 5)
    label('run')
    set(pins, 1)         
    nop()                [x]
    nop()                [x]
    out(null, 27)        [x]
    set(pins, 0)
    nop()                [x]
    jmp('run')
sm = rp2.StateMachine(0, blink, freq=100000, out_base=Pin(25))
sm.active(1)
    
    
    

def callback(data, addr, ctrl):
    if data < 0:  # NEC protocol sends repeat codes.
        print('Repeat code.')
    else:
        print('Data {:02x} Addr {:04x} Ctrl {:02x}'.format(data, addr, ctrl))
        if '{:02x}'.format(data) == '08':
            sm.put(31)
            time.sleep(1)
        if '{:02x}'.format(data) == '5a':
            sm.put(0)
            time.sleep(1)

    
    
def run(proto=0):
    ir = NEC_8(Pin(18, Pin.IN), callback)  # Instantiate receiver
    ir.error_function(print_error)  # Show debug information
    #ir.verbose = True
    # A real application would do something here...
    try:
        while True:
            print('running')
            utime.sleep(5)
            gc.collect()
    except KeyboardInterrupt:
        ir.close()


run()