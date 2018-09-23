import wolframalpha
import socket,sys,getopt
from serverVariable import app_id
from cryptography.fernet import Fernet

from src.hash import md5IsValid, unPickle, encodeMessage

def queryWolfram(question):
    client = wolframalpha.Client(app_id)
    res = client.query(question)
    answer = next(res.results).text
    return answer

def parseCommandLine(argv):
    try:
        opts, args = getopt.getopt(argv,"hp:b:z:")
    except getopt.GetoptError:
        print ('usage: server.py -p SERVER_PORT -b BACKLOG_SIZE -z SOCKET_SIZE')
        sys.exit(0)
    for opt, arg in opts:
        if opt == '-h':
            print ('usage: server.py -p SERVER_PORT -b BACKLOG_SIZE -z SOCKET_SIZE')
        elif opt == "-p":
            serverPort = int(arg)
        elif opt == "-b":
            backlogSize = int(arg)
        elif opt == "-z":
            socketSize = int(arg)
    return [serverPort,socketSize,backlogSize]


def decrypt(question,key):
    f = Fernet(key)
    decryptedQuestion = f.decrypt(question)
    return decryptedQuestion


def main(argv):
    host=''
    serverPort,socketSize,backlogSize = parseCommandLine(argv)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host,serverPort))
    s.listen(backlogSize)
    while 1:
        client, address = s.accept()
        data = client.recv(socketSize)
        key,encryptedQuestion,checkSum = unPickle(data)

        if data:
            if md5IsValid(encryptedQuestion,checkSum):
                decryptedQuestion = (decrypt(encryptedQuestion,key)).decode("utf-8")
                ans = queryWolfram(decryptedQuestion)
                payload = encodeMessage(ans)
                client.send(payload)
                client.close()
            else:
                print("Invalid CheckSum")
                sys.exit(0)      

if __name__ == '__main__':
    main(sys.argv[1:])
