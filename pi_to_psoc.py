import smbus
import time
import thread
import serial
import spidev

spi = spidev.SpiDev()
spi.open(0,0)
bus = smbus.SMBus(1)
ser = serial.Serial("/dev/ttyAMA0", timeout=1)
ser.flushInput()

address = 0x08
exit = 0

def spithread():
    while 1:
        try:
            print 'SPI Data {}'.format(spi.xfer([1,2]))
            time.sleep(1)
        except:
            time.sleep(1)
        if exit:
            thread.exit()

def uartthread():
    while 1:
        try:
            print 'UART Data {}'.format(ord(ser.read(1)))
        except:
            time.sleep(0.1)
        if exit:
            thread.exit()

def i2cthread():
    while 1:
        for i in range(0, 260, 5):
            bus.write_byte_data(address, 0, i)
            time.sleep(0.05)
        for i in range(255, 0, -5):
            bus.write_byte_data(address, 0, i)
            time.sleep(0.05)
        if exit:
            thread.exit()

try:
    thread.start_new_thread(i2cthread, ())
    thread.start_new_thread(uartthread, ())
    thread.start_new_thread(spithread, ())
except:
    print "failed"

exit = raw_input("Press Enter to exit\n")
exit = 1
time.sleep(1)
