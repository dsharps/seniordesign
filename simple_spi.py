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

def spithread():
    print "Starting SPI Thread"
    #print spi.readbytes(2)
    #print spi.readbytes(2)
    #print spi.readbytes(6)
    #print spi.xfer2([0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08])
    #print spi.xfer2([0x00]);
    i = 0
    while True:
        try:
            resp = spi.xfer2([0]);
            print resp
            time.sleep(0.05)
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
