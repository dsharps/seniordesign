import spidev
import thread
import time
import os
import OSC
import math
import sys
from collections import defaultdict
import random

spi = spidev.SpiDev()
spi.open(0, 1)
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
    #return False
    return (math.sqrt((x-128)**2 + (y-128)**2) > (deadzone * 2))


active_notes = [0, 0, 0, 0, 0, 0]
channel_to_thumbstick = {0: 35, 1: 40, 2: 49, 3: 53, 4: 8, 6: 28, 7: 23, 8: 35, 9: 40, 10: 49, 11: 53, 12: 8, 14: 28, 15: 23, 16: 34, 17: 41, 18: 54, 19: 52, 20: 9, 22: 29, 23: 22, 24: 33, 25: 41, 26: 54, 27: 52, 28: 9, 30: 29, 31: 22, 32: 34, 33: 42, 34: 55, 35: 51, 36: 10, 38: 30, 39: 21, 40: 33, 41: 42, 42: 55, 43: 51, 44: 10, 46: 30, 47: 21, 48: 32, 49: 43, 50: 56, 51: 50, 52: 11, 54: 31, 55: 20, 56: 32, 57: 43, 58: 56, 59: 50, 60: 11, 62: 31, 63: 20, 64: 27, 65: 19, 66: 44, 67: 36, 68: 4, 70: 3, 71: 12, 72: 27, 73: 19, 74: 44, 75: 36, 76: 4, 78: 3, 79: 12, 80: 26, 81: 18, 82: 45, 83: 37, 84: 5, 86: 0, 87: 13, 88: 26, 89: 18, 90: 45, 91: 37, 92: 5, 94: 0, 95: 13, 96: 25, 97: 17, 98: 46, 99: 38, 100: 6, 102: 1, 103: 14, 104: 25, 105: 17, 106: 46, 107: 38, 108: 6, 110: 1, 111: 14, 112: 24, 113: 16, 114: 47, 115: 39, 116: 7, 118: 2, 119: 15, 120: 24, 121: 16, 122: 47, 123: 39, 124: 7, 126: 2, 127: 15, -2: 48, -1: 48}
thumbstick_to_midi_pitch = {} #get David's help
active_thumbsticks = []
index = 0

banned = [5, 13, 21, 29, 37, 45, 53, 61, 69, 77, 85, 93, 101, 109, 117, 125] #Mux 5 is floating

def spithread():
    print "Starting SPI Thread"
    while True:
        try:
            #channel_data = get_all_channels()
            #hardcoded for 2 channels of polyphony, for now
            #print "X: %s, Y: %s" % (channel_data[0], channel_data[1])
            #if note_active(channel_data[0], channel_data[1]):
            #    print "X: %s, Y: %s" % (channel_data[0], channel_data[1])
            #print channel_data

            #filter to just unbanned channels
            #raw_channels = [(e, i) for e, i in enumerate(channel_data) if e not in banned]
            channel_data = random.sample(range(0, 5), 4)
            print "CD: %s" % channel_data
            print "AT: %s" % active_thumbsticks

            for d in xrange(0, len(channel_data-1, 2)):
                if len(active_thumbsticks) >= 6: #at max notes, skip the rest
                    break
                pitch = thumbstick_to_midi_pitch[channel_to_thumbstick[d]]
                if note_active(channel_data[d], channel_data[d+1]):
                    #add at index of first zero, update
                    if d not in active_thumbsticks:
                        try:
                            #get the index of the first zero, set the new pitch there
                            active_thumbsticks[active_thumbsticks.index(0)] = pitch
                        except:
                            #do nothing, try again next time
                            print "Error: %s" % sys.exc_info()
                            pass
                    #update
                    client.send(OSC.OSCMessage("/n%s"%d, [pitch, ((channel_data[d]/255.0)*10), ((channel_data[d+1]/255.0)*100),
                                           (distance_with_deadzone(channel_data[d], channel_data[d+1])/255.0)*100]))
                #note not active, but still in active_thumbsticks
                elif channel_to_thumbstick[d] in active_thumbsticks:
                    #delete this thumbstick
                    active_thumbsticks.remove(pitch)
            print "CD: %s" % channel_data
            print "AT: %s" % active_thumbsticks
            print "-------"



            # for t in raw_channels:
            #     if t[1] > 140 or t[1] < 116: #not deadzoned
            #         active_thumbsticks[channel_to_thumbstick[t[0]]] = 


            # print d
            '''print "%s, %s, %s, %s, %s, %s, %s, %s" % (bin(channel_data[0]),
                                                      bin(channel_data[1]),
                                                      bin(channel_data[2]),
                                                      bin(channel_data[3]),
                                                      bin(channel_data[4]),
                                                      bin(channel_data[5]),
                                                      bin(channel_data[6]),
                                                      bin(channel_data[7]))
            '''

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
            time.sleep(2)
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
