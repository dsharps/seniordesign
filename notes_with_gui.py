#import spidev
import thread
import time
import os
#import OSC
import math
import sys
from Tkinter import *

#spi = spidev.SpiDev()
#spi.open(0, 0)
exit = 0
count = 0

#client = OSC.OSCClient()
#client.connect(('127.0.0.1', 9002))
'''
try:
    client.send(OSC.OSCMessage("/address", 1))
except:
    print "not connected"
    pass
'''

class Example(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent, background="black")   
         
        self.parent = parent
        self.initUI()
    
    def initUI(self):
      
        self.parent.title("Joytone UI!!!")
        self.pack(fill=BOTH, expand=1)

        self.var = IntVar()
        self.label = Label(self, text=0, textvariable=self.var)        
        self.label.place(x=20, y=20)

    def update_counter(self, c):
        self.var.set(c)

deadzone = 10

def distance_with_deadzone(x, y):
    d = math.sqrt((x-128)**2 + (y-128)**2)
    if d > (deadzone * 2):
        return d
    else:
        return 0

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


def spithread():
    print "Starting SPI Thread"
    global count
    while True:
        try:
            print "Count: %s" % count
            count += 1
            time.sleep(0.5)
        except:
            print "Error: %s" % repr(sys.exc_info())
            time.sleep(0.5)
        if exit:
            thread.exit()

try:
    thread.start_new_thread(spithread, ())
except:
    print "Failed to start spithread"


root = Tk()
root.geometry("320x240+0+50")
#root.wm_overrideredirect(True)
app = Example(root)

def update_count():
    app.update_counter(count)
    root.after(200, update_count)

root.after(1000, update_count)

root.mainloop()

print "Waiting for quit signal"
exit = raw_input("Press Enter to exit\n")
exit = 1
time.sleep(1)

