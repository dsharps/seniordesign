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

def get_ordered_channels():
    resp = [94,86,110,102,126,118,78,70,76,68,92,84,108,100,124,116,4,12,20,28,36,44,52,60,79,71,95,87,111,103,127,119,121,113,105,97,89,81,73,65,55,63,39,47,23,31,7,15,120,112,104,96,88,80,72,64,14,6,30,22,46,38,62,54,56,48,40,24,32,16,8,0,75,67,91,83,107,99,123,115,1,9,17,25,33,41,49,57,74,66,90,82,106,98,122,114,122,114,10,2,51,59,35,43,19,27,3,11,26,18,42,34,58,50,5, 0]
    results = [0] * 116
    for i in xrange(0, 116):
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

def get_banned_channels():
    resp = [0, 51, 5, 13, 21, 29, 37, 45, 53, 61, 69, 77, 85, 93, 101, 109, 117, 125]
    results = [0] * 18
    for i in xrange(0, 18):
        try:
            results[i] = spi.xfer2([resp[i]])
        except:
            print "%s: %s" % (i, sys.exc_info())
    return [val for sublist in results[1:] for val in sublist]

#if the x,y position is outside of the deadzone, return true
def note_active(x, y):
    return (math.sqrt((x-128)**2 + (y-128)**2) > (deadzone * 2))


channel_to_thumbstick = {0: 35,  1: 40,  2: 49,  3: 53,  4: 8,   6: 28,  7: 23,  8: 35,  9: 40, 10: 49, 11: 53, 12: 8,  14: 28, 15: 23, 
                        16: 34, 17: 41, 18: 54, 19: 52, 20: 9,  22: 29, 23: 22, 24: 33, 25: 41, 26: 54, 27: 52, 28: 9,  30: 29, 31: 22, 
                        32: 34, 33: 42, 34: 55, 35: 51, 36: 10, 38: 30, 39: 21, 40: 33, 41: 42, 42: 55, 43: 51, 44: 10, 46: 30, 47: 21, 
                        48: 32, 49: 43, 50: 56, 51: 50, 52: 11, 54: 31, 55: 20, 56: 32, 57: 43, 58: 56, 59: 50, 60: 11, 62: 31, 63: 20, 
                        64: 27, 65: 19, 66: 44, 67: 36, 68: 4,  70: 3,  71: 12, 72: 27, 73: 19, 74: 44, 75: 36, 76: 4,  78: 3,  79: 12, 
                        80: 26, 81: 18, 82: 45, 83: 37, 84: 5,  86: 0,  87: 13, 88: 26, 89: 18, 90: 45, 91: 37, 92: 5,  94: 0,  95: 13, 
                        96: 25, 97: 17, 98: 46, 99: 38,100: 6, 102: 1, 103: 14,104: 25,105: 17,106: 46,107: 38,108: 6, 110: 1, 111: 14, 
                       112: 24,113: 16,114: 47,115: 39,116: 7, 118: 2, 119: 15,120: 24,121: 16,122: 47,123: 39,124: 7, 126: 2, 127: 15, 114: 48, 122: 48}

thumbstick_to_midi_pitch = {0: 37, 1: 42, 2: 47, 3: 39, 4: 44, 5: 49, 6: 54, 7: 59, 8: 36, 9: 41, 10: 46, 11: 51, 12: 56, 13: 61, 14: 66,
                            15: 71, 16: 38, 17: 43, 18: 48, 19: 53, 20: 58, 21: 63, 22: 68, 23: 73, 24: 35, 25: 40, 26: 45, 27: 50, 28: 55,
                            29: 60, 30: 65, 31: 70, 32: 37, 33: 42, 34: 47, 35: 52, 36: 57, 37: 62, 38: 67, 39: 72, 40: 34, 41: 39, 42: 44,
                            43: 49, 44: 54, 45: 59, 46: 64, 47: 69, 48: 46, 49: 51, 50: 56, 51: 61, 52: 66, 53: 71, 54: 58, 55: 63, 56: 68, 57: 70}
index = 0

slots = [0, 0, 0, 0, 0, 0]  #mapping of notes to slots
queue = []                  #chronological store of notes - max length should be 6!


banned = [0, 51, 5, 13, 21, 29, 37, 45, 53, 61, 69, 77, 85, 93, 101, 109, 117, 125] #Mux 5 is floating

ordered = [94,86,110,102,126,118,78,70,76,68,92,84,108,100,124,116,4,12,20,28,36,44,52,60,79,71,95,87,111,103,127,119,121,113,105,97,89,81,73,65,55,63,39,47,23,31,7,15,120,112,104,96,88,80,72,64,14,6,30,22,46,38,62,54,56,48,40,24,32,16,8,0,75,67,91,83,107,99,123,115,1,9,17,25,33,41,49,57,74,66,90,82,106,98,122,114,122,114,10,2,51,59,35,43,19,27,3,11,26,18,42,34,58,50]

def spithread():
    print "Starting SPI Thread"
    while True:
        try:
            channel_data = get_ordered_channels()
            #if note_active(channel_data[0], channel_data[1]):
            #    print "X: %s, Y: %s" % (channel_data[0], channel_data[1])
            #print channel_data[2]
            
            #print "CD: %s" % channel_data
            #print "AT: %s" % active_thumbsticks
            no_notes = True
            #print ((channel_data[len(channel_data)-1]-90)/7.0)*64
            bend = ((channel_data[len(channel_data)-1]-90)/7.0)*64
	    if 26 <= bend <= 38:
		client.send(OSC.OSCMessage("/bend", [0]))
	    else:
	        client.send(OSC.OSCMessage("/bend", [((channel_data[len(channel_data)-1]-90)/7.0)*64]))

            active_notes = [(thumbstick_to_midi_pitch[channel_to_thumbstick[d]], channel_data[d], channel_data[d+1]) for d in xrange(0, len(ordered)-1, 2) if note_active(channel_data[d], channel_data[d+1])]
            #check if a previously playing note turned off, and deactivate if so
            active_pitches = [t[0] for t in active_notes]
            for i, note in enumerate(slots):
                if note not in active_pitches:
                    client.send(OSC.OSCMessage("/n%s"%str(i), [0, 0, 0, 0])) #shutoff signal
                    slots[i] = 0 #clear slot
                    queue.remove(note) #remove from queue
                    pass

            #loop through active notes, add if necessary, then update
            for note in active_notes:
                if note[0] not in slots:
                    #add if there's a free slot, o.w. kick out oldest note and add
                    try:
                        i = slots.index(0)
                        slots[i] = note[0]
                        queue.insert(0, note[0])
                    except:
                        #catch not found exception
                        slots[slots.index(queue.pop())] = note[0]
                        queue.insert(0, note[0])
                    #add to queue also
                    pass
                #update, send note[1] and note[2]
                pass
            
            
            for d in xrange(2, len(ordered)-1, 2):
                if ordered[d] not in [100, 101] and ordered[d] not in banned:
                   # print "d:%s, t:%s" % (d, channel_to_thumbstick[ordered[d]])
                    pitch = thumbstick_to_midi_pitch[channel_to_thumbstick[ordered[d]]]
                    #pitch = 0
                    if note_active(channel_data[d], channel_data[d+1]):
                        #print "c:%s, t:%s, t2: %s, [%s, %s], p:%s" % (d, channel_to_thumbstick[ordered[d]], channel_to_thumbstick[ordered[d+1]], channel_data[d], channel_data[d+1], pitch)
                        client.send(OSC.OSCMessage("/n1", [pitch, ((channel_data[d]/255.0)*10), ((channel_data[d+1]/255.0)*100),(distance_with_deadzone(channel_data[d], channel_data[d+1])/255.0)*100]))
                        no_notes = False
                        break

            if no_notes:
                client.send(OSC.OSCMessage("/n1", [0, 0, 0, 0]))
            
            time.sleep(0.001)
        except:
            print "Error!!!: %s" % repr(sys.exc_info())
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
