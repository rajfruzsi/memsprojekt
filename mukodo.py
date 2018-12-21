#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import schedule

from twython import Twython

#Twitter fiók beállítása:
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
#Tweetelés:
def SendTweet ():
    twitter.update_status(status=message)
    print("Tweeted: {}".format(message))
#UltrhangSzenzorfüggetlen távolságmérés:
def Getdistance (PIN_TRIGGER, PIN_ECHO):
    i=0
    try:
            GPIO.setmode(GPIO.BOARD)

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
    return distance

#Tweet minden 10. percben:
schedule.every(10).minutes.do(SendTweet)

#-----------------------------------------------------------------------------
#Itt kezdődik a program

#Bekapcsoláskor beállítjuk az alap értékeket. Ehhez fogunk viszonyítani.
defaultBe=Getdistance(12,18)
defaultKi=Getdistance(26,32)

#Feltételezzük, hogy alapjáraton üres a parkoló
place=0

#Folyamatosan figyeljük halad-e el jármű a szenzorok előtt, persze hibatűréssel figyeljük.
while True:
    Be=Getdistance(12,18)
    Ki=Getdistance(26,32)
    if Be+300<defaultBe :
        place+=1
    if (Ki+300<defaultKi) and (place>0) :
        place-=1    
    message = str(Be)+"  "+str(Ki)+" "+str(defaultBe)+" "+str(defaultKi)+" --> "+str(place)
    schedule.run_pending()  
