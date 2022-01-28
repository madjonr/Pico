# Programmable I/O example with 2 unipolar steppers 28BYJ-48 + UNL2003
#  an Half Step sequence is used-  Sept 2021 - federico

from machine import Pin
from rp2 import PIO, StateMachine, asm_pio
from utime import sleep


# ====== start Input DATA =======
stepper_ratio = 1 / 64     # see stepper data sheet
cog_nr = 8                 # see stepper data sheet
# stepper motor- same colors sequence for pi pico BluePinkYellowOrange - ULN2003 BPYO
# start_pin_0 = Pin(10)      # Stepper nr.1 - 1st ( Blue color) of 4 stepper's pins
start_pin_1 = Pin(18)      # Stepper nr.2 - 1st ( Blue color) of 4 stepper's pins
nr_sm_pins = 4

# sm  2 <= kHz <= 50 this trial with unipolar stepper 28BYJ-48
frequency = 30_000         # default state machine frequency
min_frequency = 2_000      # from trials
max_frequency = 50_000     # from trials
rev_angle = 360
degrees = 360
HALF_STEP = [9, 1, 3, 2, 6, 4, 12, 8]  # see forward_PIO() & backwards_PIO()
nop_clock_delays = 32                  # see forward_PIO() & backwards_PIO()

# ====== end  Input DATA =======
steps_rev = int(cog_nr * len(HALF_STEP) * 1/stepper_ratio)
# Run the state machine for sec_rev (360 degrees) sec
sec_rev = (1 / frequency) * 2 * nop_clock_delays * steps_rev
constant = frequency * sec_rev 

# sm3.active(1);sleep(a * steps / steps_rev);sm3.active(0);sm3.exec("set(pins,0)")
k_steps = rev_angle/steps_rev
steps = int(degrees / k_steps)  # steps*k_steps = degree

# ref: GET STARTED WITH MICROPYTHON ON RASPBERRY PI PICO
#      Appendix C Programmable I/O
# program definition - the @asm_pio descriptor tells MicroPython to treat
# it as a PIO program and not a normal method
# there are 4 set pins connected to the SM, and their initial state is set
# when the StateMachine is created. 
# output low for all 4 pins ( 18,19, 20, 21)  - see sm0&sm1 instantiations for the 1st stepper
# output low for all 4 pins ( 10,11, 12, 13)  - see sm2&sm3 instantiations for the 2nd stepper

@asm_pio(set_init=(PIO.OUT_LOW,) * nr_sm_pins)  # method descriptor
def forward_PIO():   # Half step 1&2 phases
    # Step half a step to alternate between single coil and double coil steps.
    HALF_STEP = [9, 1, 3, 2, 6, 4, 12, 8]
    a = 31
    wrap_target
    # set() Drive stepper's pins as Half Step ON/OFF sequence and then delay for [a] cycles
    set(pins, HALF_STEP[0])[a]
    # nop is a pioasm pseudoinstruction used for extra delay
    nop()[a]
    set(pins, HALF_STEP[1])[a]
    nop()[a]
    set(pins, HALF_STEP[2])[a]
    nop()[a]
    set(pins, HALF_STEP[3])[a]
    nop()[a]
    set(pins, HALF_STEP[4])[a]
    nop()[a]
    set(pins, HALF_STEP[5])[a]
    nop()[a]
    set(pins, HALF_STEP[6])[a]
    nop()[a]
    set(pins, HALF_STEP[7])[a]
    nop()[a]
    wrap()

@asm_pio(set_init=(PIO.OUT_LOW,) * nr_sm_pins)
def backwards_PIO():
    HALF_STEP = [8, 12, 4, 6, 2, 3, 1, 9]
    a = 31
    wrap_target()
    set(pins, HALF_STEP[0])[a]
    nop()[a]
    set(pins, HALF_STEP[1])[a]
    nop()[a]
    set(pins, HALF_STEP[2])[a]
    nop()[a]
    set(pins, HALF_STEP[3])[a]
    nop()[a]
    set(pins, HALF_STEP[4])[a]
    nop()[a]
    set(pins, HALF_STEP[5])[a]
    nop()[a]
    set(pins, HALF_STEP[6])[a]
    nop()[a]
    set(pins, HALF_STEP[7])[a]
    nop()[a]
    wrap()

# 1st stepper
# sm0 = StateMachine(0,    forward_PIO, freq=frequency, set_base=start_pin_0)
# sm1 = StateMachine(1,  backwards_PIO, freq=frequency, set_base=start_pin_0)

# 2nd stepper
sm2 = StateMachine(2,    forward_PIO, freq=frequency, set_base=start_pin_1)
sm3 = StateMachine(3,  backwards_PIO, freq=frequency, set_base=start_pin_1)

#-------------------------- END of Code------------------------------------

#***** Run examples ******
a = (constant / frequency)
degrees = 360
print("State Machine Hz = ", frequency, " ", a * degrees / rev_angle, " sec for ", degrees, " degrees")

# sm0.active(1)  # start the stepper nr1
sm3.active(1)  # start the stepper nr3

# Run the state machine for a * degrees / rev_angle seconds
sleep(a * degrees / rev_angle)

# sm0.active(0)  # stop the sm0 - 1st stepper
sm3.active(0)  # stop the sm3 - 2nd stepper

# Turn off the set pins ( 4 pico/stepper pins) via an exec instruction.
# sm0.exec("set(pins,0)")
sm3.exec("set(pins,0)")

sleep(1)

# sm0.active(1); sleep(512 * constant/(frequency*steps_rev));sm0.active(0); sm0.exec("set(pins,0)")
# sm1.active(1); sleep(512 * constant/(frequency*steps_rev));sm1.active(0); sm1.exec("set(pins,0)")
sm2.active(1); sleep(512 * constant/(frequency*steps_rev));sm2.active(0); sm2.exec("set(pins,0)")
sm3.active(1); sleep(512 * constant/(frequency*steps_rev));sm3.active(0); sm3.exec("set(pins,0)")

# sm0.active(1); sleep(1024 * constant/(frequency*steps_rev));sm0.active(0); sm0.exec("set(pins,0)")
# sm1.active(1); sleep(1024 * constant/(frequency*steps_rev));sm1.active(0); sm1.exec("set(pins,0)")
sm2.active(1); sleep(1024 * constant/(frequency*steps_rev));sm2.active(0); sm2.exec("set(pins,0)")
sm3.active(1); sleep(1024 * constant/(frequency*steps_rev));sm3.active(0); sm3.exec("set(pins,0)")

# sm0.active(1); sleep(2048 * constant/(frequency*steps_rev));sm0.active(0); sm0.exec("set(pins,0)")
# sm1.active(1); sleep(2048 * constant/(frequency*steps_rev));sm1.active(0); sm1.exec("set(pins,0)")
sm2.active(1); sleep(2048 * constant/(frequency*steps_rev));sm2.active(0); sm2.exec("set(pins,0)")
sm3.active(1); sleep(2048 * constant/(frequency*steps_rev));sm3.active(0); sm3.exec("set(pins,0)")

# sm0.active(1); sm3.active(1); sleep(512 * constant/(frequency*steps_rev));sm0.active(0);sm3.active(0); sm0.exec("set(pins,0)"); sm3.exec("set(pins,0)")
# sm1.active(1); sm2.active(1); sleep(512 * constant/(frequency*steps_rev));sm1.active(0);sm2.active(0); sm1.exec("set(pins,0)"); sm2.exec("set(pins,0)")

#---------------------------------------------------------------------------------------
sleep(1)
print( "to change the stepper speed we change the State Machine Hz with a new State Machine instantiation")

frequency = 50000
sec_rev = (1 / frequency) * 2 * nop_clock_delays * steps_rev
constant = frequency * sec_rev 
a = (constant / frequency)
degrees = 360

# sm1 = StateMachine(0,    forward_PIO, freq= frequency, set_base=start_pin_0)
sm3 = StateMachine(3,    forward_PIO, freq= frequency, set_base=start_pin_1)

print("State Machine Hz = ", frequency, " ", a * degrees / rev_angle, " sec for ", degrees, " degrees")

# sm1.active(1)  # start the stepper nr1
sm3.active(1)  # start the stepper nr2

# Run the state machine for a * degrees / rev_angle seconds
sleep(a * degrees / rev_angle)

# sm1.active(0)  # stop the sm1 - 1st stepper
sm3.active(0)  # stop the sm3 - 2nd stepper

# Turn off the set pins ( 4 pico/stepper pins) via an exec instruction.
# sm1.exec("set(pins,0)")
sm3.exec("set(pins,0)")

sleep(1)

print("********** 1st Stepper Forward ****************")
# sm0 = StateMachine(0,    forward_PIO, freq=frequency, set_base=start_pin_0)
# sm0.active(1);sleep(degrees * a  / rev_angle);sm0.active(0);sm0.exec("set(pins,0)")
print("********** 1st Stepper Backward ****************")
# sm1 = StateMachine(1,  backwards_PIO, freq=frequency, set_base=start_pin_0)
# sm1.active(1);sleep(degrees * a  / rev_angle);sm1.active(0);sm1.exec("set(pins,0)")

sleep(1)

print("********** 2nd Stepper Forward ****************")
sm2 = StateMachine(2,    forward_PIO, freq=frequency, set_base=start_pin_1)
sm2.active(1);sleep(degrees * a  / rev_angle);sm2.active(0);sm2.exec("set(pins,0)")
print("********** 2nd Stepper Backward ****************")
sm3 = StateMachine(3,  backwards_PIO, freq=frequency, set_base=start_pin_1)
sm3.active(1);sleep(degrees * a  / rev_angle);sm3.active(0);sm3.exec("set(pins,0)")


print(" use of steps in place of degrees")
sm3.active(1);sleep(2048 * a / steps_rev);sm3.active(0);sm3.exec("set(pins,0)")
sleep(1)
sm3.active(1);sleep(1024 * a  / steps_rev);sm3.active(0);sm3.exec("set(pins,0)")
sleep(1)
sm3.active(1);sleep(512 * a  / steps_rev);sm3.active(0);sm3.exec("set(pins,0)")
sleep(1)
sm3.active(1);sleep(512 * a  / steps_rev);sm3.active(0);sm3.exec("set(pins,0)")



