import smbus
import time
import thread
import serial
import spidev

spi = spidev.SpiDev()
spi.open(0,0)
bus = smbus.SMBus(1)
#ser = serial.Serial("/dev/ttyAMA0", timeout=1)
#ser.flushInput()

address = 0x08
exit = 0
#count = 0
#current_time = time.time()

def spithread():
    while 1:
        try:
            print 'SPI Data {}'.format(spi.xfer([1,2,3,4,5,6,7,8,9,10,
                                                 11,12,13,14,15,16,17,18,19,20,
                                                 21,22,23,24,25,26,27,28,29,30,
                                                 31,32,33,34,35,36,37,38,39,40,
                                                 41,42,43,44,45,46,47,48,49,50]))   
            time.sleep(0.005)
        except:
            time.sleep(0.005)
        if exit:
            thread.exit()

#def uartthread():
#    while 1:
#        try:
#            print 'UART Data {}'.format(ord(ser.read(1)))
#        except:
#            time.sleep(0.1)
#        if exit:
#            thread.exit()

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
    #thread.start_new_thread(uartthread, ())
    thread.start_new_thread(spithread, ())
except:
    print "failed"

exit = raw_input("Press Enter to exit\n")
exit = 1
#print "Count: %s, Time: %s, Rate: %s" % (count, time.time()-current_time, (count / (time.time() - current_time)))
time.sleep(1)
