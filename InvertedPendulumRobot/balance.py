

def class Balance:
    
    __init__(self, setpoint):
        self.setpoint = setpoint
    
    
    def __call__(self, angle, gyro):
        bias = 0
        balance_KP = 10
        balance_KD = 2
        balance = 0
        bias = angle - self.setpotin
        balance = balance_KP * bias + balance_KD * gyro
        return balance 