//based off of Gordon Henderson's gpio test code

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <wiringPi.h>

// LEDs:

#define GREEN      0

// The input button

#define BUTTON     8

int lightIsOn = 0;

/*
 * setup:
 *  Program the GPIO correctly and initialise the lamps
 ***********************************************************************
 */

void setup (void)
{
  if (geteuid () != 0)
  {
    fprintf (stderr, "Need to be root to run (sudo?)\n") ;
    exit (0) ;
  }

  if (wiringPiSetup () == -1)
    exit (1) ;

  printf ("Setup ... ") ; fflush (stdout) ;
  // for (i = 0 ; i < 5 ; ++i)
  // {
  //   pinMode (i, OUTPUT) ;
  //   digitalWrite (i, 0) ;
  // }
  // digitalWrite (GREEN, 1) ;
  // digitalWrite (RED_MAN, 1) ;
  // pinMode (BUTTON, INPUT) ;

  pinMode (GREEN, OUTPUT);
  pinMode (BUTTON, INPUT);

  printf ("OK\n") ;
}

/*
 * waitButton:
 *  Wait for the button to be pressed. Because we have the GPIO
 *  pin pulled high, we wait for it to go low to indicate a push.
 ***********************************************************************
 */

void waitButton (void)
{
  printf ("Waiting for button ... ") ; fflush (stdout) ;
  while (digitalRead (BUTTON) == HIGH)
    delay (100) ;
  printf ("Got it\n") ;
}

void toggleLight (void)
{
  printf("Toggling the light") ; fflush(stdout) ;
  if (lightIsOn)
  {
    digitalWrite(GREEN, 0);
    lightIsOn = 0;
  }
  else
  {
    digitalWrite(GREEN, 1);
    lightIsOn = 1;
  }
}


/*
 ***********************************************************************
 * The main program
 *  Call our setup routing once, then sit in a loop, waiting for
 *  the button to be pressed then executing the sequence.
 ***********************************************************************
 */

int main (void)
{
  setup () ;
  for (;;)
  {
    waitButton   () ;
    toggleLight  () ;
    delay(1000);
  }
}