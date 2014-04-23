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

#if the x,y position is outside of the deadzone, return true
def note_active(x, y): 
    #return False
    return (math.sqrt((x-128)**2 + (y-128)**2) > (deadzone * 2))

#four-note polyphony
pitches = [0, 0, 0, 0]

def spithread():
    print "Starting SPI Thread"
    while True:
        try:
            channel_data = get_32_channels()
            #hardcoded for 2 channels of polyphony, for now
            #print "X: %s, Y: %s" % (channel_data[0], channel_data[1])
            #if note_active(channel_data[0], channel_data[1]):
            #    print "X: %s, Y: %s" % (channel_data[0], channel_data[1])
    
            #check note 1
            if note_active(channel_data[0], channel_data[1]):
                if pitches[0] == 0:
                    #turn on note
                    print "Activating Note 60"
                    pitches[0] = 60
                    client.send(OSC.OSCMessage("/p1", 60))
                client.send(OSC.OSCMessage("/tune1", ((channel_data[0]/255.0)*50)))
                client.send(OSC.OSCMessage("/lop1", ((channel_data[1]/255.0)*127)))
                client.send(OSC.OSCMessage("/vol1", distance_with_deadzone(channel_data[0], channel_data[1])))
            else:
                if pitches[0] != 0:
                    #turn off note
                    print "Deactivating Note 60"
                    pitches[0] = 0
                    client.send(OSC.OSCMessage("/p1", 0))
                    client.send(OSC.OSCMessage("/vol1", 0))

            #check note 2
            if note_active(channel_data[2], channel_data[3]):
                if pitches[1] == 0:
                    #turn on note
                    print "Activating Note 67"
                    pitches[1] = 67
                    client.send(OSC.OSCMessage("/p2", 67))
                client.send(OSC.OSCMessage("/tune2", ((channel_data[2]/255.0)*50)))
                client.send(OSC.OSCMessage("/lop2", ((channel_data[3]/255.0)*127)))
                client.send(OSC.OSCMessage("/vol2", distance_with_deadzone(channel_data[2], channel_data[3])))
            else:
                if pitches[1] != 0:
                    #turn off note
                    print "Deactivating Note 67"
                    pitches[1] = 0
                    client.send(OSC.OSCMessage("/p2", 0))
                    client.send(OSC.OSCMessage("/vol2", 0))
                        
            '''client.send(OSC.OSCMessage("/p1", get_hip(60)))
            client.send(OSC.OSCMessage("/lop1", get_lop(channel_data[0])))
            client.send(OSC.OSCMessage("/volume1", distance_with_deadzone(channel_data[0], channel_data[1])))
            client.send(OSC.OSCMessage("/pwm1", get_pwm(channel_data[1])))'''
            
            time.sleep(0.001)
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
