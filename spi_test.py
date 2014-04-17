import spidev
import thread
import time
import os
import OSC
import math
import sys

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

deadzone = 10

def distance_with_deadzone(x, y):
    d = math.sqrt((x-128)**2 + (y-128)**2)
    if d > (deadzone * 2):
        return d
    else:
        return 0

def get_hip(y):
    if (y > 128 + deadzone):
        return ((y - 128) / 128.0) * 4000
    return 0

def get_lop(y):
    if (y < 128 - deadzone):
        return (y / 128.0) * 4000
    return 4000

def get_pwm(x):
    return (x/255.0)*100

def get_32_channels():
    resp = [0, 8, 16, 24, 32, 40, 48, 56, 64, 72, 80, 88, 96, 104, 112, 120,
            1, 9, 17, 25, 33, 41, 49, 57, 65, 73, 81, 89, 97, 105, 113, 121, 0]
    results = [0] * 33
    for i in xrange(0, 33):
        try:
            results[i] = spi.xfer2([resp[i]])
        except:
            print sys.exc_info()
    return [val for sublist in results[1:] for val in sublist]
    

def spithread():
    print "Starting SPI Thread"
    while True:
        try:
            channel_data = get_32_channels()
            #print channel_data
            client.send(OSC.OSCMessage("/hip1", get_hip(channel_data[0])))
            client.send(OSC.OSCMessage("/lop1", get_lop(channel_data[0])))
            client.send(OSC.OSCMessage("/volume1", distance_with_deadzone(channel_data[0], channel_data[1])))
            client.send(OSC.OSCMessage("/pwm1", get_pwm(channel_data[1])))
            
            '''client.send(OSC.OSCMessage("/hip2", get_hip(channel_data[2])))
            client.send(OSC.OSCMessage("/lop2", get_lop(channel_data[2])))
            client.send(OSC.OSCMessage("/volume2", distance_with_deadzone(channel_data[2], channel_data[3])))
            client.send(OSC.OSCMessage("/pwm2", get_pwm(channel_data[3])))

            client.send(OSC.OSCMessage("/hip3", get_hip(channel_data[4])))
            client.send(OSC.OSCMessage("/lop3", get_lop(channel_data[4])))
            client.send(OSC.OSCMessage("/volume3", distance_with_deadzone(channel_data[4], channel_data[5])))
            client.send(OSC.OSCMessage("/pwm3", get_pwm(channel_data[5])))

            client.send(OSC.OSCMessage("/hip4", get_hip(channel_data[6])))
            client.send(OSC.OSCMessage("/lop4", get_lop(channel_data[6])))
            client.send(OSC.OSCMessage("/volume4", distance_with_deadzone(channel_data[6], channel_data[7])))
            client.send(OSC.OSCMessage("/pwm4", get_pwm(channel_data[7])))'''
            
            time.sleep(0.01)
        except:
            print "Error"
            time.sleep(0.1)
        if exit:
            thread.exit()

try:
    thread.start_new_thread(spithread, ())
except:
    print "failed"
    
exit = raw_input("Press Enter to exit\n")
exit = 1
time.sleep(1)
