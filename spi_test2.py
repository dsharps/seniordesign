import spidev
import thread
import time
import os
import OSC
import math

spi = spidev.SpiDev()
spi.open(0, 0)
exit = 0

client = OSC.OSCClient()
client.connect(('127.0.0.1', 9002))

try:
    client.send(OSC.OSCMessage("/address", 1))
except:
    print "not connected"
    pass

deadzone = 55

def distance_with_deadzone(x, y):
    d = math.sqrt((x-1023)**2 + (y-1023)**2)
    if d > (deadzone * 2):
        return d
    else:
        return 0

def get_hip(y):
    if (y > 1023 + deadzone):
        return ((y - 1023) / (1023.0 + deadzone) * 4000)
    return 0

def get_lop(y):
    if (y < 1023 - deadzone):
        return (y / (1023.0 - deadzone) * 4000)
    return 4000

def get_pwm(x):
    return (x/2048.0)*100

def spithread():
    print "Starting SPI Thread"
    num = 0;
    #print spi.xfer2([0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])
    #print spi.xfer2([0xAA, 0xAA])
    #print spi.readbytes(2)
    #print spi.readbytes(2)
    #print spi.readbytes(6)
    #print spi.xfer2([0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08])
    print spi.xfer2([0x00]);
    while True:
        try:
            #resp = spi.xfer2([0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08])
            #resp = spi.readbytes(6)
            #xpos = resp[0]
            #ypos = resp[1]

            resp = spi.xfer2([num]);
            if (resp[0] != num-1):
                print "%s : %s" % (num, resp)
            
            #print resp
            num+=1
            if num > 127:
                print "---------"
                num = 0
            
            #client.send(OSC.OSCMessage("/hip1", get_hip(ypos)))
            #client.send(OSC.OSCMessage("/lop1", get_lop(ypos)))
            #client.send(OSC.OSCMessage("/volume1", distance_with_deadzone(xpos, ypos)))
            #client.send(OSC.OSCMessage("/pwm1", get_pwm(xpos)))
            #print "hip: %s, lop: %s, volume: %s, pwm: %s" % (get_hip(ypos), \
                                                             #get_lop(ypos), \
                                                             #distance_with_deadzone(xpos, ypos), \
                                                             #get_pwm(xpos))
            time.sleep(0.1)
        except:
            time.sleep(0.001)
        if exit:
            spi.close()
            thread.exit()

try:
    thread.start_new_thread(spithread, ())
except:
    print "failed"
    
exit = raw_input("Press Enter to exit\n")
exit = 1
time.sleep(1)
