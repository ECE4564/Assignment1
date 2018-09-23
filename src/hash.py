
import hashlib
from fernet import Fernet

def md5(bytestr):
    return hashlib.md5(bytestr).hexdigest()

def check_positive(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError("%s must be a positive int value" % value)
    return ivalue

def decodeMessage(data):
    data = pickle.loads(data)
    key = data[0]
    enc_data = data[1]
    md5_hash = data[2]
    return (key, enc_data, md5_hash)


def get_check_question(data):
    key, enc_data, md5_hash = decodeMessage(data)
    if md5_hash != md5(enc_data):
        print("Hash incorrect")
    else:
        print('[Checkpoint] Checksum is VALID')
    f = Fernet(key)

    print('[Checkpoint] Decrypt: Using Key: ', key, 'Plaintext: ', f.decrypt(enc_data).decode())

    return (key, f.decrypt(enc_data).decode())
