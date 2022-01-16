from machine import UART, Pin
import _thread
import utime

recv_buf = ""


print("-- ESP8266 Webserver --")
print("setting up UART Connection...")

uart = UART(0, tx=Pin(12), rx=Pin(13), baudrate=115200, bits=8, parity=None, stop=1)
print("done!")



def uartSerialRxMonitor():
    prvMills = utime.ticks_ms()
    recv = b""
    while (utime.ticks_ms()-prvMills)<2000:
        if uart.any():
            recv = b"".join(recv, uart.read(1))
            print(recv)
            #print(recv, end='')
            global recv_buf
            recv_buf += recv
    try:
        print(recv.decode())
    except UnicodeError:
        print(recv)
        


print("Staring connection to ESP8266...")
_thread.start_new_thread(uartSerialRxMonitor, ())  # start serial monitor as thread
print("done!")


print("Setting up network on ESP8266...")
print("  - Setting CWMODE to 1 station mode...")
uart.write('AT+CWMODE=2\r\n')                 # 设置无线模式AP，STA， sta/AP 三种
utime.sleep(1000)

print("  - Join Wifi ...")
uart.write('AT+CWJAP="ChinaNet-xmZc","iSi89cwwVdxmmZc"\r\n')  # set Wifi network SSID and PWD here
utime.sleep(2000)
print("done!\r\n")

print("Starting Webserver port on ESP8266...")
utime.sleep(2000)
print('  - Setting CIPMUX for multiple connections...')
uart.write('AT+CIPMUX=1\r\n')    # 0单连接模式，1多连接模式
utime.sleep(1000)

print("  - Starting CIPSERVER on port 80...")
uart.write('AT+CIPSERVER=1,80\r\n')
print('done!')
utime.sleep(1000)

print('Waiting For connection...')
while True:
    if '+ID' in recv_buf:    # IPD in serial indicates an incoming connection
        utime.sleep(2000)
        print("! Incoming connection - sending webpage")
        # Send a HTTP respone then a webpage as bytes the 108 is the amount of bytes you are sending,
        # change this if you change the data sent below
        uart.write('AT+CIPSEND=0,108\r\n')
        utime.sleep(1000)
        uart.write('HTTP/1.1 200 OK\r\n')
        uart.write('Content-Type: text/html\r\n')
        uart.write('Connection: close\r\n')
        uart.write('\r\n')
        uart.write('<!DOCTYPE HTML>\r\n')
        uart.write('<html>\r\n')
        uart.write('It Works!\r\n')
        uart.write('</html>\r\n')
        utime.sleep(1000)
        uart.write('AT+CIPCLOSE=0\r\n')     # close the connection when done.
        utime.sleep(4000)
        print(' ')
        print(' ')
        print('Waiting For connection... ')
        recv_buf = ""



































