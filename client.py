import os
import tweepy
import pickle
import socket,sys,getopt
from tweepy import Stream
from tweepy.streaming import StreamListener

from src.clientargparser import client_parser

from clientVariable import *

from src.hash import md5IsValid, encodeMessage

def deconstruct(Data):
    return pickle.loads(Data)

def decrypt(question,key):
    f = Fernet(key)
    decryptedQuestion = f.decrypt(question)
    return decryptedQuestion

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

        #assemble stripped tweet payload
        payload = encodeMessage(tweet.replace(hash_tag, ''))

        print("C1")

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        print("C2")

        s.bind((bridge_ip, bridge_port))

        print("C3")

        s.listen(socket_size)

        print("C4")

        bridge, address = s.accept()

        print("C5")

        bridge.send(payload)

        print("C6")

        data = bridge.recv(socket_size)

        print("C7")

        key,encryptedAnswer,checkSum = deconstruct(data)

        print("D")

        if data:
            if md5IsValid(encryptedAnswer,checkSum):
                decryptedAnswer = (decrypt(encryptedAnswer,key)).decode("utf-8")
                print(decryptedAnswer)
            else:
                print("Invalid CheckSum")
                sys.exit(0)

        print("E")
        return True

args = client_parser().parse_args()

bridge_ip = args.bridge_ip
bridge_port = int(args.bridge_port)
socket_size = int(args.socket_size)
hash_tag = args.hash_tag

print(bridge_ip, bridge_port, socket_size, hash_tag)

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.secure = True
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

customListener = filterListener()
customStream = Stream(api.auth, customListener)
customStream.filter(track=[hash_tag])
