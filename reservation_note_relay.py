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

def get_12_channels():
    resp = [0, 8, 16, 24, 32, 40, 48, 56, 64, 72, 80, 88, 60, 52, 44, 36, 0]
    results = [0] * 13
    for i in xrange(0, 13):
        try:
            results[i] = spi.xfer2([resp[i]])
        except:
            print sys.exc_info()
    return [val for sublist in results[1:] for val in sublist]

def get_all_channels():
    resp = [i for i in xrange(0, 129)]
    results = [0] * 129
    for i in xrange(0, 129):
        try:
            results[i] = spi.xfer2([resp[i]])
        except:
            print sys.exc_info()
    return [val for sublist in results[1:] for val in sublist]

def get_special_channels():
    resp = [0, 8, 16, 24, 32, 40, 48, 56, 60, 52, 44, 36, 0]
    results = [0] * 13
    for i in xrange(0, 13):
        try:
            results[i] = spi.xfer2([resp[i]])
        except:
            print "%s: %s" % (i, sys.exc_info())
    return [val for sublist in results[1:] for val in sublist]

def get_digital_channels():
    resp = [128, 129, 130, 131, 132, 133, 134, 135, 0]
    results = [0] * 9
    for i in xrange(0, 9):
        try:
            results[i] = spi.xfer2([resp[i]])
        except:
            print "%s: %s" % (i, sys.exc_info())
    return [val for sublist in results[1:] for val in sublist]

#if the x,y position is outside of the deadzone, return true
def note_active(x, y): 
    return False
    return (math.sqrt((x-128)**2 + (y-128)**2) > (deadzone * 2))

#three-note polyphony
active_notes = 0
pitches = [0, 0, 0, 0, 0, 0]
midi_notes = [48, 50, 51, 52, 53, 55]

def spithread():
    print "Starting SPI Thread"
    while True:
        try:
            channel_data = get_digital_channels()
            #hardcoded for 2 channels of polyphony, for now
            #print "X: %s, Y: %s" % (channel_data[0], channel_data[1])
            #if note_active(channel_data[0], channel_data[1]):
            #    print "X: %s, Y: %s" % (channel_data[0], channel_data[1])
            #print channel_data
            print channel_data
            print "%s, %s, %s, %s, %s, %s, %s, %s" % (bin(channel_data[0]),
                                                      bin(channel_data[1]),
                                                      bin(channel_data[2]),
                                                      bin(channel_data[3]),
                                                      bin(channel_data[4]),
                                                      bin(channel_data[5]),
                                                      bin(channel_data[6]),
                                                      bin(channel_data[7]))
            '''
            #check note 1
            if note_active(channel_data[0], channel_data[1]):
                if pitches[0] == 0:
                    #turn on note
                    print "Activating Note 48"
                    pitches[0] = 48
                client.send(OSC.OSCMessage("/n1", [48, ((channel_data[0]/255.0)*10), ((channel_data[1]/255.0)*100),
                                           (distance_with_deadzone(channel_data[0], channel_data[1])/255.0)*100]))
            else:
                if pitches[0] != 0:
                    #turn off note
                    print "Deactivating Note 48"
                    pitches[0] = 0
                    client.send(OSC.OSCMessage("/n1", [48, 0, 0, 0]))

            #check note 2
            if note_active(channel_data[2], channel_data[3]):
                if pitches[1] == 0:
                    #turn on note
                    print "Activating Note 50"
                    pitches[1] = 50
                client.send(OSC.OSCMessage("/n2", [50, ((channel_data[2]/255.0)*10), ((channel_data[3]/255.0)*100),
                                           (distance_with_deadzone(channel_data[2], channel_data[3])/255.0)*100]))
            else:
                if pitches[1] != 0:
                    #turn off note
                    print "Deactivating Note 50"
                    pitches[1] = 0
                    client.send(OSC.OSCMessage("/n2", [50, 0, 0, 0]))

            #check note 3
            if note_active(channel_data[4], channel_data[5]):
                if pitches[2] == 0:
                    #turn on note
                    print "Activating Note 51"
                    pitches[2] = 51
                client.send(OSC.OSCMessage("/n3", [51, ((channel_data[4]/255.0)*10), ((channel_data[5]/255.0)*100),
                                           (distance_with_deadzone(channel_data[4], channel_data[5])/255.0)*100]))
            else:
                if pitches[2] != 0:
                    #turn off note
                    print "Deactivating Note 51"
                    pitches[2] = 0
                    client.send(OSC.OSCMessage("/n3", [51, 0, 0, 0]))

            #check note 4
            if note_active(channel_data[6], channel_data[7]):
                if pitches[3] == 0:
                    #turn on note
                    print "Activating Note 52"
                    pitches[3] = 51
                client.send(OSC.OSCMessage("/n4", [52, ((channel_data[6]/255.0)*10), ((channel_data[7]/255.0)*100),
                                           (distance_with_deadzone(channel_data[6], channel_data[7])/255.0)*100]))
            else:
                if pitches[3] != 0:
                    #turn off note
                    print "Deactivating Note 52"
                    pitches[3] = 0
                    client.send(OSC.OSCMessage("/n4", [52, 0, 0, 0]))

            #check note 5
            if note_active(channel_data[8], channel_data[9]):
                if pitches[4] == 0:
                    #turn on note
                    print "Activating Note 53"
                    pitches[4] = 53
                client.send(OSC.OSCMessage("/n5", [53, ((channel_data[8]/255.0)*10), ((channel_data[9]/255.0)*100),
                                           (distance_with_deadzone(channel_data[8], channel_data[9])/255.0)*100]))
            else:
                if pitches[4] != 0:
                    #turn off note
                    print "Deactivating Note 53"
                    pitches[4] = 0
                    client.send(OSC.OSCMessage("/n5", [53, 0, 0, 0]))

            #check note 6
            if note_active(channel_data[10], channel_data[11]):
                if pitches[5] == 0:
                    #turn on note
                    print "Activating Note 55"
                    pitches[5] = 55
                client.send(OSC.OSCMessage("/n6", [55, ((channel_data[10]/255.0)*10), ((channel_data[11]/255.0)*100),
                                           (distance_with_deadzone(channel_data[10], channel_data[11])/255.0)*100]))
            else:
                if pitches[5] != 0:
                    #turn off note
                    print "Deactivating Note 55"
                    pitches[5] = 0
                    client.send(OSC.OSCMessage("/n6", [55, 0, 0, 0]))
            '''
            time.sleep(0.5)
        except:
            print "Error: %s" % repr(sys.exc_info())
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
