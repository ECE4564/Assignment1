
import hashlib
import pickle
from fernet import Fernet
import datetime


def time():
    return "[" + str(datetime.datetime.time(datetime.datetime.now()))[:8] + "]"

def md5(bytestr):
    return hashlib.md5(bytestr).hexdigest()

def md5IsValid(encryptedQuestion,md5):
    return md5 is md5(encryptedQuestion)

def decryptMessage(data, key):
    f = Fernet(key)
    return f.decrypt(data).decode()

def encryptMessage(data, key):
    f = Fernet(key)
    return f.encrypt(data).decode()

def unPickle(data):
    return pickle.loads(data)

def decodeMessage(data):
    key = data[0]
    enc_data = data[1]
    md5_hash = data[2]
    return (key, enc_data, md5_hash)

def encodeMessage(data):
    key = Fernet.generate_key()
    f = Fernet(key)
    return pickle.dumps((key, f.encrypt(data), md5(f.encrypt(data))))
