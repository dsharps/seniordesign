import os
import time

print "Setting up sound card"
os.system("sudo modprobe snd_bcm2835")
os.system("sudo amixer cset numid=3 1")
print "Launching pd"
os.system("pd -nogui PolySynth.pd")
