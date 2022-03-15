from machine import Pin, I2C, PWM, UART, ADC
import utime
from imu import MPU6050

_MAXSPEED = const(11000)
_MINSPEED = const(10)
_MAXPITCH = const(25)    # Any more than this means we have fallen over
_PWM_DUTY = const(10000) # 32767=50% PWM duty cycle with 500us pulsewidth, 10000=15% & 150us pw, 5000=7.5% & 76us pw
_RUN      = const(0) 
_STOP     = const(1)
_D_ENPIN  = const(9)
_L_DIRPIN = const(0)     
_L_DRIVE  = const(1)
_R_DIRPIN = const(10)  
_R_DRIVE  = const(11) 
_LED_1    = 25
_VOLT_CONV= 12.6 / 65535 # 12.6v is max for a fully charged 3S LiPo pack 电池最大电压
_MIN_VOLTS= 10.5 # Min voltage for a 3S LiPo pack 电池最小电压

left_dir = Pin(_L_DIRPIN, Pin.OUT, Pin.PULL_DOWN) 
right_dir = Pin(_R_DIRPIN, Pin.OUT, Pin.PULL_DOWN) 
drive_enable = Pin(_D_ENPIN, Pin.OUT, Pin.PULL_DOWN) 
left_pwm = PWM(Pin(_L_DRIVE, Pin.OUT))        
right_pwm = PWM(Pin(_R_DRIVE, Pin.OUT))
left_pwm.duty_ns(_PWM_DUTY) 
right_pwm.duty_ns(_PWM_DUTY)      
drive_enable.value(_STOP)
onboard_led = machine.Pin(_LED_1, machine.Pin.OUT)

# Allow the BNO055 IMU to initialise
utime.sleep(1)

# Set up bluetooth comms
#uart = UART(id=_BT_ID, baudrate=_BT_BAUD, bits=_BT_BITS, parity=_BT_PARITY, stop=_BT_STOP, tx=_BT_TX, rx=_BT_RX)

# Set up the IMU
i2c = I2C(1, sda=Pin(26), scl=Pin(27), freq=400000)
imu = MPU6050(i2c)

# Interpolate the value from the PID controller for the PWM output. Output scale is _MINSPEED to _MAXSPEED
def interpolate_pid(value, inMin, inMax) -> int:
    return int(max(min(_MAXSPEED, (value - inMin) * (_MAXSPEED - _MINSPEED) // (inMax - inMin) + _MINSPEED), _MINSPEED))

kP = 0.1              # PID P value
kI = 0.01                # PID I value
kD = 0.01               # PID D Value
previous = 0         # Variable value for pid
integral = 0         # Variable value for pid
calibration = 0      # Adjustment value for the center of gravity in deg - tweak to make "error" zero when vertical
fwd_rev = 0          # Value to shift balance and create movement via remote, in degrees
f_r = 0
l_bias = 0           # Holds left steering bias from bluetooth
r_bias = 0           # Hols right steering bias from bluetooth

while True:    
    pitch = imu.gyro.y                                            # Get euler roll value [0=heading, 1=roll, 2=pitch]
    print(pitch)
    error = pitch + calibration + fwd_rev                             # Add calibration and forward/reverse to measured pitch angle
    integral += error                                       # Add error to PID integral value
    pid_output = error * kP + integral * kI + (error - previous) * kD # PID calculation
    print('pid_output:{}'.format(pid_output))
    if pid_output > 0:                                                # Leaning forwards
        current_speed = (interpolate_pid(pid_output, 1000, 0))        # Interpolate PID controller to PWM values
        print('curent_speed:{}'.format(current_speed))
        left_dir.value(1)
        right_dir.value(1)
    else:                                                             # Leaning backwards
        current_speed = (interpolate_pid(pid_output, 0, -1000))       # Interpolate PID controller to PWM values
        print('curent_speed:{}'.format(current_speed))
        left_dir.value(0)
        right_dir.value(0)
        
    if (abs(pitch) <= _MAXPITCH):                                     # We have not fallen over so proceed
        drive_enable.value(_RUN)                                      # Enable drive outputs
        left_pwm.freq(current_speed)                         # Set left motor speed
        right_pwm.freq(current_speed)                        # Set right motor speed
        
        previous = error                                              # Store current error for PWM derivative value
    utime.sleep_ms(20)
        
        
        
        
        