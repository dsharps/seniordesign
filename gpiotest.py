from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

GPIO.setup(16, GPIO.IN)
GPIO.setup(18, GPIO.IN)

GPIO.setup(11, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)
GPIO.output(11, GPIO.LOW)
GPIO.output(13, GPIO.LOW)
GPIO.output(15, GPIO.LOW)

# state - decides what LED should be on and off
state = 0

# increment - the direction of states
inc = 1

while True:

    # state toggle button is pressed
        if ( GPIO.input(16) == True ):

        if (inc == 1):
            state = state + 1;
        else:
            state = state - 1;

        # reached the max state, time to go back (decrement)
        if (state == 3):
            inc = 0
        # reached the min state, go back up (increment)
        elif (state == 0):
            inc = 1

        if (state == 1):
            GPIO.output(11, GPIO.HIGH)
            GPIO.output(13, GPIO.LOW)
            GPIO.output(15, GPIO.LOW)
        elif (state == 2):
            GPIO.output(11, GPIO.HIGH)
            GPIO.output(13, GPIO.HIGH)
            GPIO.output(15, GPIO.LOW)
        elif (state == 3):
            GPIO.output(11, GPIO.HIGH)
            GPIO.output(13, GPIO.HIGH)
            GPIO.output(15, GPIO.HIGH)
        else:
            GPIO.output(11, GPIO.LOW)
            GPIO.output(13, GPIO.LOW)
            GPIO.output(15, GPIO.LOW)
        print("pressed B1 ", state)

    # reset button is pressed
        if ( GPIO.input(18) == True ):

        state = 0
        inc = 1
        GPIO.output(11, GPIO.LOW)
        GPIO.output(13, GPIO.LOW)
        GPIO.output(15, GPIO.LOW)

        print("pressed B2 ", state)

        sleep(0.2);