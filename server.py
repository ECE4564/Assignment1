import wolframalpha
import hashlib
import socket,sys,getopt
from serverVariable import key
from serverVariable import app_id
from cryptography.fernet import Fernet

def parseCommandLine(argv):
    try:
        opts, args = getopt.getopt(argv,"hp:b:z:")
    except getopt.GetoptError:
        print ('usage: server.py -p SERVER_PORT -b BACKLOG_SIZE -z SOCKET_SIZE')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('usage: server.py -p SERVER_PORT -b BACKLOG_SIZE -z SOCKET_SIZE')
        elif opt == "-p":
            serverPort = arg
        elif opt == "-b":
            backlogSize = arg
        elif opt == "-z":
            socketSize = arg
    return [serverPort,socketSize,backlogSize]


def decrypt(question):
    f = Fernet(key)
    decryptedQuestion = f.decrypt(question)
    return decryptedQuestion


# def main(argv):
def main():
    host=''
    # serverPort,socketSize,backlogSize = parseCommandLine(argv)
    # print("backlogSize: ",backlogSize)
    # print("socketSize: ",socketSize)
    # print("serverPort: ",serverPort)
    # questionString  = input("Question: ")
    # #changing questionString to bytes
    # questionBytes = questionString.encode()

    serverPort=50000
    socketSize=1024
    backlogSize =5

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host,serverPort))
    s.listen(backlogSize)
    while 1:
        client, address = s.accept()
        data = client.recv(socketSize)
        if data:
            client.send(data)
            client.close()

    # f = Fernet(key)
    # token = f.encrypt(questionBytes)

    # questionString1 = decrypt(token)
    # client = wolframalpha.Client(app_id)
    # res = client.query(questionString1)
    # answer = next(res.results).text
    # print(answer)

if __name__ == '__main__':
    # main(sys.argv[1:])
    main()