import imp
import A4988
from machine import Pin
import utime

class Motor42(A4988):
    """
    
    """

    

    def __init__(self, step, direction, ms1, ms2, ms3):
        super(Motor42, self).__init__(step, direction, ms1, ms2, ms3)


    def run(self):
        pass

    def change_diretion(self):
        pass

    def speed_control(self, speed):
        pass