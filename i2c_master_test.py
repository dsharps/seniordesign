import smbus
import time
# for RPI version 1, use "bus = smbus.SMBus(0)"
bus = smbus.SMBus(1)

# This is the address we setup in the Arduino Program
address = 0x04

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

while True:
    print "Reading from Arduino"

    x_low = bus.read_byte(address)
    x_high = bus.read_byte(address)
    y_low = bus.read_byte(address)
    y_high = bus.read_byte(address)
    
    print "x_low: %s, x_high: %s, y_low: %s, y_high: %s" % (x_low, x_high, y_low, y_high)

    print "X: %s, Y: %s" % (x_low + (x_high << 8), y_low + (y_high << 8))
    # sleep one second
    time.sleep(1)

    print "----------------"
