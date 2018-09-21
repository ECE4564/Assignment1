from src.clientargparser import client_parser

from clientVariable import key

from clientVariable import consumer_key
from clientVariable import consumer_secret

from clientVariable import access_token
from clientVariable import access_token_secret

import os
import tweepy
from tweepy import Stream
from tweepy.streaming import StreamListener

#override tweepy.StreamListener to add logic to on_status
class filterListener(StreamListener):
    def on_status(self, status):
        if hasattr(status, 'retweeted_status'):
            try:
                tweet = status.retweeted_status.extended_tweet["full_text"]
            except:
                tweet = status.retweeted_status.text
        else:
            try:
                tweet = status.extended_tweet["full_text"]
            except AttributeError:
                tweet = status.text

        stripped_tweet = tweet.replace(hash_tag, '')

        print(tweet)
        return True

args = client_parser().parse_args()

bridge_ip = args.bridge_ip
bridge_port = args.bridge_port
socket_size = args.socket_size
hash_tag = args.hash_tag

print(bridge_ip, bridge_port, socket_size, hash_tag)

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.secure = True
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

customListener = filterListener()
customStream = Stream(api.auth, customListener)
customStream.filter(track=[hash_tag])
