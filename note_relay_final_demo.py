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
    return (math.sqrt((x-128)**2 + (y-128)**2) > (deadzone * 2))


active_notes = [0, 0, 0, 0, 0, 0]
channel_to_thumbstick = {0: 35, 1: 40, 2: 49, 3: 53, 4: 8, 6: 28, 7: 23, 8: 35, 9: 40, 10: 49, 11: 53, 12: 8, 14: 28, 15: 23, 16: 34, 17: 41, 18: 54, 19: 52, 20: 9, 22: 29, 23: 22, 24: 33, 25: 41, 26: 54, 27: 52, 28: 9, 30: 29, 31: 22, 32: 34, 33: 42, 34: 55, 35: 51, 36: 10, 38: 30, 39: 21, 40: 33, 41: 42, 42: 55, 43: 51, 44: 10, 46: 30, 47: 21, 48: 32, 49: 43, 50: 56, 51: 50, 52: 11, 54: 31, 55: 20, 56: 32, 57: 43, 58: 56, 59: 50, 60: 11, 62: 31, 63: 20, 64: 27, 65: 19, 66: 44, 67: 36, 68: 4, 70: 3, 71: 12, 72: 27, 73: 19, 74: 44, 75: 36, 76: 4, 78: 3, 79: 12, 80: 26, 81: 18, 82: 45, 83: 37, 84: 5, 86: 0, 87: 13, 88: 26, 89: 18, 90: 45, 91: 37, 92: 5, 94: 0, 95: 13, 96: 25, 97: 17, 98: 46, 99: 38, 100: 6, 102: 1, 103: 14, 104: 25, 105: 17, 106: 46, 107: 38, 108: 6, 110: 1, 111: 14, 112: 24, 113: 16, 114: 47, 115: 39, 116: 7, 118: 2, 119: 15, 120: 24, 121: 16, 122: 47, 123: 39, 124: 7, 126: 2, 127: 15, -2: 48, -1: 48}
thumbstick_to_midi_pitch = {0: 37, 1: 42, 2: 47, 3: 39, 4: 44, 5: 49, 6: 54, 7: 59, 8: 36, 9: 41, 10: 46, 11: 51, 12: 56, 13: 61, 14: 66,
                            15: 71, 16: 38, 17: 43, 18: 48, 19: 53, 20: 58, 21: 63, 22: 68, 23: 73, 24: 35, 25: 40, 26: 45, 27: 50, 28: 55,
                            29: 60, 30: 65, 31: 70, 32: 37, 33: 42, 34: 47, 35: 52, 36: 57, 37: 62, 38: 67, 39: 72, 40: 34, 41: 39, 42: 44,
                            43: 49, 44: 54, 45: 59, 46: 64, 47: 69, 48: 46, 49: 51, 50: 56, 51: 61, 52: 66, 53: 71, 54: 58, 55: 63, 56: 68, 57: 70}
active_thumbsticks = [0, 0, 0, 0, 0, 0]
index = 0

banned = [5, 13, 21, 29, 37, 45, 53, 61, 69, 77, 85, 93, 101, 109, 117, 125] #Mux 5 is floating

def spithread():
    global active_thumbsticks
    print "Starting SPI Thread"
    while True:
        try:
            channel_data = get_all_channels()
            #if note_active(channel_data[0], channel_data[1]):
            #    print "X: %s, Y: %s" % (channel_data[0], channel_data[1])
            #print channel_data
            
            #print "CD: %s" % channel_data
            #print "AT: %s" % active_thumbsticks

            for d in xrange(0, len(channel_data)-1, 2):
                print "d:%s, t:%s" % (d, channel_to_thumbstick[d])
                pitch = thumbstick_to_midi_pitch[channel_to_thumbstick[d]]
                #pitch = 0
                print "checking active"
                if note_active(channel_data[d], channel_data[d+1]):
                    #add at index of first zero, update
                    print "checking d"
                    if d not in active_thumbsticks and active_thumbsticks.index(0) != -1:
                        print "d not found"
                        try:
                            #get the index of the first zero, set the new pitch there
                            active_thumbsticks[active_thumbsticks.index(0)] = pitch
                        except:
                            #do nothing, try again next time
                            print "Error!!: %s" % repr(sys.exc_info())
                            pass
                    #update
                    #client.send(OSC.OSCMessage("/n%s"%d, [pitch, ((channel_data[d]/255.0)*10), ((channel_data[d+1]/255.0)*100),
                    #                       (distance_with_deadzone(channel_data[d], channel_data[d+1])/255.0)*100]))
                #note not active, but still in active_thumbsticks
                elif not note_active(channel_data[d], channel_data[d+1]) and channel_to_thumbstick[d] in active_thumbsticks:
                    #delete this thumbstick
                    print "removing d"
                    active_thumbsticks.remove(pitch)
                    #shut off OSC
            print "CD: %s" % channel_data
            print "AT: %s" % active_thumbsticks
            print "-------"

            time.sleep(2)
                                      
            '''print "%s, %s, %s, %s, %s, %s, %s, %s" % (bin(channel_data[0]),
                                                      bin(channel_data[1]),
                                                      bin(channel_data[2]),
                                                      bin(channel_data[3]),
                                                      bin(channel_data[4]),
                                                      bin(channel_data[5]),
                                                      bin(channel_data[6]),
                                                      bin(channel_data[7]))
            '''
            time.sleep(3)
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
