from twython import Twython
from keksz import(
    distance
    )

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
message = distance
twitter.update_status(status=message)
print("Tweeted: {}".format(message))
