import smbus
import time
#import libpd as pd
import os
import OSC
import math

# for RPI version 1, use "bus = smbus.SMBus(0)"
bus = smbus.SMBus(1)

# This is the address we setup in the Arduino Program
address = 0x04

# Init OSC
client = OSC.OSCClient()
client.connect(('127.0.0.1', 9002)) # first argument is the IP of the host, second argument is the port to use

try:
    client.send(OSC.OSCMessage("/address", 1)) # first argument is what we could call the OSC adress of the data, second argument is the actual data to be sent.
except:
    print "not connected"
    pass

def writeNumber(value):
    bus.write_byte(address, value)
    # bus.write_byte_data(address, 0, value)
    return -1

def readX():
    x_pos = bus.read_byte(address)
    return x_pos

def readY():
    y_pos = bus.read_byte(address)
    return y_pos


def send_to_pd(message=''):
    #os.system("echo '" + message + "'| pdsend 3000")
    pass

def audio_on():
    message = '0 1;' #id 0 is dsp, 1 = turn on
    send_to_pd(message)

def audio_off():
    message = '0 0;' #id o is dsp, 0 = turn off
    send_to_pd(message)

def set_frequency(frequency):
    message = '1 ' + repr(frequency) + ';'
    send_to_pd(message)

def distance_with_deadzone(x, y):
    d = math.sqrt((x-512)**2 + (y-512)**2)
    if d > 65:
        return d
    else:
        return 0

audio_on()
xpos = 0
ypos = 0

while True:
    #print "Reading from Arduino"

    x_low = bus.read_byte(address)
    x_high = bus.read_byte(address)
    y_low = bus.read_byte(address)
    y_high = bus.read_byte(address)

    xpos = (x_low + (x_high << 8))
    ypos = (y_low + (y_high << 8))
    
    #print "x_low: %s, x_high: %s, y_low: %s, y_high: %s, | %s, %s" % (x_low, x_high, y_low, y_high, xpos, ypos)

    #print "X: %s, Y: %s" % (xpos, ypos)
    # sleep one second
    if xpos > 600:
        audio_on()
    else:
        audio_off()

    client.send(OSC.OSCMessage("/frequency", ypos))
    client.send(OSC.OSCMessage("/volume", distance_with_deadzone(xpos, ypos)))
    client.send(OSC.OSCMessage("/timbre", xpos))
    #set_frequency(ypos)
    time.sleep(0.001)

    #print "----------------"
