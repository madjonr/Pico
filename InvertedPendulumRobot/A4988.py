
STEPS = {
    'FULL': 1,
    'HALF':2,
    'QUATER':4,
    'EIGHTH':8,
    'SIXTEENTH':16
}


class A4988(object):
    """
    a4988控制步进电机类
    """
    def __init__(self, ms1, ms2, ms3, enable=None):
        """
        初始化引脚信息
        """
        #self.step = step                           # 步数引脚
        #self.direction = direction                 # 方向引脚
        self.ms1 = ms1                             # 电机细分ms1引脚
        self.ms2 = ms2                             # 电机细分ms2引脚
        self.ms3 = ms3                             # 电机细分ms3引脚
        self.enable = enable                       # 使能引脚



    def set_steps(self, step):
        if step == STEPS.get('FULL'):
            self.ms1.low()
            self.ms2.low()
            self.ms3.low()
        elif step == STEPS.get('HALF'):
            self.ms1.high()
            self.ms2.low()
            self.ms3.low()
        elif step == STEPS.get('QUATER'):
            self.ms1.low()
            self.ms2.high()
            self.ms3.low()
        elif step == STEPS.get('EIGHTH'):
            self.ms1.high()
            self.ms2.high()
            self.ms3.low()
        else:
            self.ms1.high()
            self.ms2.high()
            self.ms3.high()
            
            




