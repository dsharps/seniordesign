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

def distance_with_deadzone(x, y):
    d = math.sqrt((x-1023)**2 + (y-1023)**2)
    if d > 65:
        return d
    else:
        return 0

def spithread():
    print "Starting SPI Thread"
    while True:
        try:
            resp = spi.xfer2([1, 2, 3, 4])
            xpos = (resp[0] << 8) + resp[1]
            ypos = (resp[2] << 8) + resp[3]
            client.send(OSC.OSCMessage("/frequency", ypos))
            client.send(OSC.OSCMessage("/volume", distance_with_deadzone(xpos, ypos)))
            client.send(OSC.OSCMessage("/timbre", xpos))
            #print "X: %s, Y: %s" % (xpos, ypos)
            time.sleep(0.001)
        except:
            time.sleep(0.001)
        if exit:
            thread.exit()

try:
    thread.start_new_thread(spithread, ())
except:
    print "failed"
    
exit = raw_input("Press Enter to exit\n")
exit = 1
time.sleep(1)
