#!/usr/bin/env python

from twython import Twython
twitter = Twython

consumer_key = 'pZq6xYSByzpDF9YnbiOoB0bcp'  
consumer_secret= 'Y4loC8w1yQPIf4mZ7X5zHNmMfc6DG6YLU1QTYusypTfhZ4KXZS'
access_key= '1060151021962477569-9Bb5SiPWOnEJuOkMRbNfa08lCXVdMA'
access_secret = 'gKWnozDlYIzKtHi6jxU2sMwOT41PU5iGuRd7ojBQN7p9X'


message = "Hello world!"
twitter.update_status(status=message)
print("Tweeted: {}".format(message))



