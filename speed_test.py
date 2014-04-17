import smbus
import time
import thread
import serial
import spidev
import sys

spi = spidev.SpiDev()
spi.open(0,0)
bus = smbus.SMBus(1)
#ser = serial.Serial("/dev/ttyAMA0", timeout=1)
#ser.flushInput()

address = 0x08
count = 0
successes = 0
errors = 0
fails = 0
current_time = time.time()

l = [x for x in xrange(0, 50)]
r = l
r.insert(0, r.pop())
t = [0x00]
b = 0x00
data = [0]*32
while count < 1000:
    try:
        #print 'SPI Data {}'.format(spi.xfer([1,2,3,4,5,6,7,8,9,10,
        #                                     11,12,13,14,15,16,17,18,19,20,
        #                                     21,22,23,24,25,26,27,28,29,30,
        #                                     31,32,33,34,35,36,37,38,39,40,
        #                                     41,42,43,44,45,46,47,48,49,50]))   
        #t = [x for x in xrange(0, 8)]
        #t[0] = b
        #print "t: %s" % t
        #spi.xfer2(t)
        #print "r: %s" % t
        #print "-------"
        '''if (t[0] == b-1 or (t[0] == 127 and b == 0)):
            successes += 1
        else:
            errors += 1
            #print t
        count += 
        b += 1
        if b > 127:
            b = 0
        '''
        resp = [0, 0, 8, 16, 24, 32, 40, 48, 56, 64, 72, 80, 88, 96, 104, 112, 120,
               1, 9, 17, 25, 33, 41, 49, 57, 65, 73, 81, 89, 97, 105, 113, 121]
        
        for x in xrange(0, 32):
            data[x] = spi.xfer2([resp[x]])
            #print "Value %s: %s" % (x, spi.xfer2([resp[x]]))
        data = [value for sublist in data for value in sublist]
        print data[:8]
        #print spi.xfer2([resp[2]])
        #print spi.xfer([resp[3]])
        time.sleep(0.001)
    except:
        fails += 1
        print "Error: %s" % (repr(sys.exc_info()))
        time.sleep(0.5)

print "Count: %s, Successes: %s, Errors: %s, Fails: %s, \nTime: %s, Rate: %s" % (count, successes, errors, fails, time.time()-current_time, (count / (time.time() - current_time)))
time.sleep(1)
