#!/usr/bin/python

import RPi.GPIO as GPIO
import time

from twython import Twython


from auth1 import (
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
)
twitter = Twython(
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
)


#while 0==0:
try:
          GPIO.setmode(GPIO.BOARD)

          PIN_TRIGGER = 12
          PIN_ECHO = 18

          GPIO.setup(PIN_TRIGGER, GPIO.OUT)
          GPIO.setup(PIN_ECHO, GPIO.IN)

          GPIO.output(PIN_TRIGGER, GPIO.LOW)

          print ("Waiting for sensor to settle")

          time.sleep(2)

          print ("Calculating distance")

          GPIO.output(PIN_TRIGGER, GPIO.HIGH)

          time.sleep(0.00001)

          GPIO.output(PIN_TRIGGER, GPIO.LOW)

          while GPIO.input(PIN_ECHO)==0:
                pulse_start_time = time.time()
          while GPIO.input(PIN_ECHO)==1:
                pulse_end_time = time.time()

          pulse_duration = pulse_end_time - pulse_start_time
          distance = round(pulse_duration * 17150, 2)
          print(distance)

finally:
          GPIO.cleanup()

message = distance
twitter.update_status(status=message)
print("Tweeted: {}".format(message))
