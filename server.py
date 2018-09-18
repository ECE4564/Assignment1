import wolframalpha
import hashlib
import socket,sys,getopt
from serverVariable import key
from serverVariable import app_id
from cryptography.fernet import Fernet

def decrypt(question):
    f = Fernet(key)
    decryptedQuestion = f.decrypt(question)
    return decryptedQuestion


def main(argv):
    serverPort = ''
    backlogSize= ''
    socketSize = ''
    try:
        opts, args = getopt.getopt(argv,"hp:b:z:")
    except getop  t.GetoptError:
        print ('server.py -p <SERVER_PORT> -b <BACKLOG_SIZE> -z <SOCKET_SIZE>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('server.py -p <SERVER_PORT> -b <BACKLOG_SIZE> -z <SOCKET_SIZE>')
        elif opt == "-p":
            serverPort = arg
        elif opt == "-b":
            backlogSize = arg
        elif opt == "-z":
            socketSize = arg
    print("backlogSize: ",backlogSize)
    print("socketSize: ",socketSize)
    print("serverPort: ",serverPort)

    questionString  = input("Question: ")
    questionBytes = questionString.encode()

    f = Fernet(key)
    token = f.encrypt(questionBytes)

    questionString1 = decrypt(token)
    client = wolframalpha.Client(app_id)
    res = client.query(questionString1)
    answer = next(res.results).text
    print(answer)

if __name__ == '__main__':
    main(sys.argv[1:])