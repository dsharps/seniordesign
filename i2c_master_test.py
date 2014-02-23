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

    x_pos = readX();
    y_pos = readY();

    print "X: %s, Y: %s" % (x_pos, y_pos)
    # sleep one second
    time.sleep(1)

    print "----------------"