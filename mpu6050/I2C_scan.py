import machine
sdaPIN=machine.Pin(26)
sclPIN=machine.Pin(27)
i2c=machine.I2C(1,sda=sdaPIN, scl=sclPIN, freq=400000)

print('Scanning i2c bus')
devices = i2c.scan()    # 扫出来的是连接上I2C总线设备的地址

if len(devices) == 0:
    print("No i2c device !")
else:
    print('i2c devices found:',len(devices))

for device in devices:
    print("Decimal address: ",device," | Hexa address: ",hex(device))