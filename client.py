import os
import tweepy
import pickle
import socket,sys,getopt
from tweepy import Stream
from tweepy.streaming import StreamListener

from src.clientargparser import client_parser

from clientVariable import *

from src.hash import md5IsValid, encodeMessage, time

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

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        s.bind((bridge_ip, bridge_port))
        # [ Checkpoint  01]  Connecting  to <BRIDGE IP>  on  port <BRIDGE PORT #>
        print(time() + "[ Checkpoint  01] Connecting  to " + bridge_ip + " on  port " + bridge_port)

        s.listen(socket_size)
        
        print(time() +"C4")

        bridge, address = s.accept()

        print(time() +"C5")

        bridge.send(payload)

        print(time() +"C6")

        data = bridge.recv(socket_size)

        print(time() +"C7")

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

# [ Checkpoint  01] Checking arguments: <BRIDGE_IP> : <BRIDGE_PORT> : <SOSCKET_SIZE> : <HASHTAG>
print(time() + "arguments: BridgeIP: " bridge_ip," | Bridge port: ", bridge_port, " | socket size: ",socket_size," | hashtag: ", hash_tag)

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.secure = True
auth.set_access_token(access_token, access_token_secret)


api = tweepy.API(auth)

customListener = filterListener()
customStream = Stream(api.auth, customListener)
# [ Checkpoint  02]  Listening  f o r  Tweets  that  contain : <HASHTAG>

customStream.filter(track=[hash_tag])

while True:
    count = 0


# [ Checkpoint  01]  Connecting  to <BRIDGE IP>  on  port <BRIDGE PORT #>
# [ Checkpoint  02]  Listening  f o r  Tweets  that  contain : <HASHTAG>
# [ Checkpoint  03] New Tweet : <TWITTER_QUESTION>
# [ Checkpoint  04]  Encrypt :  Generated Key : <ENCRYPTION KEY>|  Ciphertext :<ENCRYPTED QUESTION>
# [ Checkpoint  05]  Sending  data : <QUESTION PAYLOAD>
# [ Checkpoint  06]  Received  data : <ANSWER PAYLOAD>
# [ Checkpoint  07]  Decrypt :  Using Key : <ENCRYPTION KEY>|  Plaintext : <DECRYPTED ANSWER>
