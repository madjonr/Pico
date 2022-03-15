from mpu6050 import MPU6050
import utime

mpu = MPU6050(1, 26, 27, (2244, -740, 1238, 49, -51, 9))

if mpu.passed_self_test:
    while True:
        ax, ay, az, gx, gy, gz = mpu.data