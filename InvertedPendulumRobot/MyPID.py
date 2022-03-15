
import utime


class PID:
    
    def __init__(self, Kp=1.0, Ki=0.0, Kd=0.0, setpoint=0, sample_time=0.01, output_limits=(None, None)):
        """
        Initialize a new PID controller.
        param:
            Kp: P系数，控制比例增益的值 
            Ki: I系数，控制积分增益的值
            Kd: D系数，控制微分增益的值
            setpoint: 目标值
            sample_time: 采样间隔时间
            output_limits: 输出值限制范围
        """
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.setpoint = setpoint
        self.sample_time = sample_time
        self._min_output, self._max_output = None, None


        self._proportional = 0                  # 比例系数
        self._integral = 0                      # 积分
        self._derivative = 0                    # 微分

        self._last_time = None                  # 最后一次采样时间
        self._last_output = None                # 最后一次输出
        self._last_input = None                 # 最后一次输入

        self.output_limits = output_limits      
        self.reset()
        
        


    def PD(self, setpoint, angle, gyro):
        '''
        直立PD环
        '''
        error = 0
        balance = 0
        error = angle - setpoint
        speed = self.Kp * error + self.Kd * gyro
        return speed
    
    
    def PI(self, input_):
        now = utime.ticks_ms()
        if dt is None:                           # 微分时的时间步长
            dt = now - self._last_time if (now - self._last_time) else 1e-16
        elif dt <= 0:
            raise ValueError('dt has negative value {}, must be positive'.format(dt))

        if self.sample_time is not None and dt < self.sample_time and self._last_output is not None:
            # Only update every sample_time seconds
            return self._last_output

        # Compute error terms
        # 计算误差
        error = self.setpoint - input_

        # Compute integral and derivative terms
        self._integral += self.Ki * error * dt
        self._integral = _clamp(self._integral, self.output_limits)  # Avoid integral windup
        # Compute final output
        output = self._proportional + self._integral
        output = _clamp(output, self.output_limits)

        # Keep track of state
        self._last_output = output
        self._last_input = input_
        self._last_time = now

        return output
        
        
    
    
    def PID(self, angle):
        now = utime.ticks_ms()
        if dt is None:                           # 微分时的时间步长
            dt = now - self._last_time if (now - self._last_time) else 1e-16
        elif dt <= 0:
            raise ValueError('dt has negative value {}, must be positive'.format(dt))

        if self.sample_time is not None and dt < self.sample_time and self._last_output is not None:
            # Only update every sample_time seconds
            return self._last_output

        # Compute error terms
        # 计算误差
        error = self.setpoint - input_
        d_input = input_ - (self._last_input if (self._last_input is not None) else input_)  # 输入的增量

        # Check if must map the error
        if self.error_map is not None:
            error = self.error_map(error)

        # Compute the proportional term
        if not self.proportional_on_measurement:
            # Regular proportional-on-error, simply set the proportional term
            self._proportional = self.Kp * error
        else:
            # Add the proportional error on measurement to error_sum
            self._proportional -= self.Kp * d_input

        # Compute integral and derivative terms
        self._integral += self.Ki * error * dt
        self._integral = _clamp(self._integral, self.output_limits)  # Avoid integral windup

        self._derivative = -self.Kd * d_input / dt

        # Compute final output
        output = self._proportional + self._integral + self._derivative
        output = _clamp(output, self.output_limits)

        # Keep track of state
        self._last_output = output
        self._last_input = input_
        self._last_time = now

        return output
    
    
    
    