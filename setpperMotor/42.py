from machine import Pin, ADC
import utime
import rp2
import gc
from nec import NEC_8, NEC_16
from print_error import print_error  

motoA_step = Pin(10)
motoA_direction = Pin(9, Pin.OUT)
motoA_ms1 = Pin(11, Pin.OUT)
motoA_ms2 = Pin(12, Pin.OUT)
motoA_ms3 = Pin(13, Pin.OUT)

motoA_ms1.high()
motoA_ms2.high()
motoA_ms3.high()


motoB_step = Pin(17)
motoB_direction = Pin(16, Pin.OUT)
motoB_ms1 = Pin(6, Pin.OUT)
motoB_ms2 = Pin(7, Pin.OUT)
motoB_ms3 = Pin(8, Pin.OUT)

motoB_ms1.high()
motoB_ms2.high()
motoB_ms3.high()


freq_test = 100000

# To control speed just modify the amount/value of nop[dely amount 0-31].
@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW, out_shiftdir=rp2.PIO.SHIFT_RIGHT)
def runA():
    wrap_target()
    set(pins, 1)         [31]
    nop()                [10]
    nop()                [10]
    set(pins, 0)         [31]
    nop()                [10]
    nop()                [10]
    wrap()
    
    
# To control speed just modify the amount/value of nop[dely amount 0-31].
@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW, autopull=True)
def runB():
    wrap_target()
    set(pins, 1)   [1]
    #nop()          [1]
    #nop()          [1]
    set(pins, 0)   [1]
    #nop()          [1]
    #nop()          [1]
    wrap()


"""Instantiate a state machine with the move
program, at 100000Hz, with set base to step pin."""
motorA = rp2.StateMachine(0, runA, freq=freq_test, set_base=motoA_step)
motorB = rp2.StateMachine(1, runB, freq=freq_test, set_base=motoB_step)

# Set direction
motoA_direction.value(0)
motoB_direction.value(0)

# Start your motor!
motorA.active(1)
# Start your motor!
motorB.active(1)

motorA.put(31)


    


def callback(data, addr, ctrl):
    if data < 0:  # NEC protocol sends repeat codes.
        print('Repeat code.')
    else:
        print('Data {:02x} Addr {:04x} Ctrl {:02x}'.format(data, addr, ctrl))
        if '{:02x}'.format(data) == '08':
            print('->')
            motorA.active(0)
            motorB.active(0)
            utime.sleep_ms(100)
            motoA_direction.value(0)
            motoB_direction.value(0)
            motorA.active(1)
            motorB.active(1)
        if '{:02x}'.format(data) == '5a':
            motorA.active(0)
            motorB.active(0)
            utime.sleep_ms(100)
            motoA_direction.value(1)
            motoB_direction.value(1)
            motorA.active(1)
            motorB.active(1)
            print('<-')
        if '{:02x}'.format(data) == '18':
            motorA.put(31)
            if motorA.tx_fifo():
                print('put seccessed! {}'.format(motorA.tx_fifo()))
        if '{:02x}'.format(data) == '52':
            motorA.put(1)
            if motorA.tx_fifo():
                print('put seccessed! {}'.format(motorA.tx_fifo()))
    
    
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


# run()