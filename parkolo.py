#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import schedule
import smtplib, ssl

from twython import Twython

capacity=50

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
def SendEmail():
    port = 465
    smtp_server = "smtp.gmail.com"
    sender_email = "memsprojekt@gmail.com"  
    receiver_email = "memsprojekt@gmail.com" 
    password = input("Adja meg a jelszavat, es nyomjon entert: ")
    messageout= """\
    Subject: Parking lot space

    The number of cars in the parking lot is """+str(parking)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, messageout)

#UltrhangSzenzorfüggetlen távolságmérés:
def Getdistance (PIN_TRIGGER, PIN_ECHO):
    i=0
    try:
            GPIO.setmode(GPIO.BOARD)

            GPIO.setup(PIN_TRIGGER, GPIO.OUT)
            GPIO.setup(PIN_ECHO, GPIO.IN)

            GPIO.output(PIN_TRIGGER, GPIO.LOW)

            print ("Waiting for sensor to settle")

            time.sleep(1.5)

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

#Tweet minden percben:
schedule.every(30).minutes.do(SendTweet)
schedule.every(30).minutes.do(SendEmail)

#-----------------------------------------------------------------------------
#Itt kezdődik a program

#Bekapcsoláskor beállítjuk az alap értékeket. Ehhez fogunk viszonyítani.
defaultBe=Getdistance(12,18)
defaultKi=Getdistance(26,32)

#Feltételezzük, hogy alapjáraton üres a parkoló
parking=0
#Automatikus hibaküszöbbeállítás
if (defaultBe<15):
    h1=1
elif (defaultBe<50):
    h1=5
elif (defaultBe<500):
    h1=100 
else:
    h1=300

if (defaultKi<15):
    h2=1
elif (defaultKi<50):
    h2=5
elif (defaultKi<500):
    h2=100
else:
    h2=300
#Folyamatosan figyeljük halad-e el jármű a szenzorok előtt, persze hibatűréssel figyeljük.
while True:
    Be=Getdistance(12,18)
    Ki=Getdistance(26,32)
    localtime = time.asctime( time.localtime(time.time()) )
    if (Be+h1<defaultBe) and (parking<capacity) :
        parking+=1
    if (Ki+h2<defaultKi) and (parking>0) :
        parking-=1    
    message = "Kedves parkolni vágyók!"+ "\n"+"A parkolóban jelenleg "+str(parking)+ " db autó tartózkodik" + "\n"+"Még "+ str(capacity-parking)+ " db szabad hely van"+ "\n\n"+localtime
    schedule.run_pending()
