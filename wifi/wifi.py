import os, sys
import utime
import machine

#print sys info
print(os.uname())

rx0=machine.Pin(13) #RPI PICO GPI1
tx0=machine.Pin(12) #RPI PICO GPI0 

#print uart info
uart = machine.UART(0, tx=tx0, rx=rx0, baudrate=115200,bits=8, parity=None, stop=1)
print(uart)

led_onboard = machine.Pin(25, machine.Pin.OUT)
led_onboard.value(0)     # onboard LED OFF for 0.5 sec
utime.sleep(0.5)
led_onboard.value(1)


def sendCMD_waitResp(cmd, uart=uart, timeout=2000):
    print("CMD: " + cmd)
    uart.write(cmd)
    waitResp(uart, timeout)
    print()
    
def waitResp(uart=uart, timeout=2000):
    prvMills = utime.ticks_ms()
    resp = b""
    while (utime.ticks_ms()-prvMills)<timeout:
        if uart.any():
            resp = b"".join([resp, uart.read(1)])
    print("resp:")
    try:
        print(resp.decode())
    except UnicodeError:
        print(resp)           

            

waitResp()
sendCMD_waitResp("AT\r\n")       # 测试模块状态
sendCMD_waitResp("AT+GMR\r\n")   # 查看版本信息


utime.sleep(0.5)
sendCMD_waitResp("AT+RST\r\n") #RESET ESP8266 重启

sendCMD_waitResp("AT+CWMODE=2\r\n")  # 设置AP模式
utime.sleep(0.5)
sendCMD_waitResp("AT+CIPMUX=1\r\n")      # 启用多连接
utime.sleep(0.5)
sendCMD_waitResp('AT+CWSAP="ESP8266","12345678",3,4\r\n',  timeout=5000) #设置AP的SSID PWD 信道和加密方式
utime.sleep(5)
#sendCMD_waitResp("AT+CIPSTATUS\r\n")   # 查看网络连接信息，作为sta的时候
sendCMD_waitResp("AT+CIPSERVER=1,80\r\n")    # 启动TCP服务器，IP地址默认，端口为80
sendCMD_waitResp("AT+CWLIF\r\n")        # 查看当前连接到AP的客户端列表

print("connected........")
print("RPi-PICO with esp8266")
while True:
    if uart.any()>0:
      respon = uart.readline()
      print (respon)
      print ( "lose....." )
    