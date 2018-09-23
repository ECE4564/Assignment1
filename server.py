import wolframalpha
import socket,sys,getopt
from serverVariable import app_id
from cryptography.fernet import Fernet
from src.hash import md5IsValid, unPickle, encodeMessage, time

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

    serverPort,socketSize,backlogSize = parseCommandLine(argv)
    
    #[ Checkpoint  0]  Received argument list <ARGS>
    print(time() + "[Checkpoint 00] Arguments received ",(serverPort,socketSize,backlogSize))
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((socket.gethostname(),serverPort))
    s.listen(backlogSize)

    #[ Checkpoint  01]  Created  socket  at  0.0.0.0  on  port <BRIDGE_PORT>
    print(time() + "[Checkpoint 01] Created socket at 0.0.0.0  on  port {0}".format(serverPort))
    
    
    while 1:
        # Wait for data from client
        print(time() + "[Checkpoint 02] Listening  for  client connections")

        client, address = s.accept()

        # [Checkpoint 03] Accepted client connection  from BRIDGE_IP  on  port <BRIDGE_PORT>
        print(time() + "[Checkpoint 03] Accepted client connection  from", address[0], 'on port', address[1])

        data = client.recv(socketSize)

        # [ Checkpoint  04]  Received  data : <PICKLED DATA>
        print(time() + "[Checkpoint 04] Received data: ", data)


        key,encryptedQuestion,checkSum = unPickle(data)

        if data:
            
            # [ Checkpoint  05]  Validating CheckSum for Data : <MD5>
            print(time() + "[Checkpoint 05] Received data checkSum: ", checkSum)

            if md5IsValid(encryptedQuestion,checkSum):
                decryptedQuestion = (decrypt(encryptedQuestion,key)).decode("utf-8")

                # [ Checkpoint  06]  Wolfram  Question  : <QUESTION>
                print(time() + "[ Checkpoint  06]  Wolfram  Question  :", decryptedQuestion)

                ans = queryWolfram(decryptedQuestion)

                # [ Checkpoint  07]  Wolfram  Question  : <QUESTION>
                print(time() + "[ Checkpoint  07]  Wolfram  Answer  :", ans)

                payload = encodeMessage(ans)

                # [ Checkpoint  08]  Encoding Answer  : <ANSWER PAYLOAD>
                print(time() + "[ Checkpoint  08]  Answer Payload  :", payload)

                client.send(payload)

                # [ Checkpoint  08]  Sending Data  : <ANSWER>
                print(time() + "[ Checkpoint  08]  Sending Answer  :", payload)

                # client.close()
            else:
                print("Invalid CheckSum")

if __name__ == '__main__':
    main(sys.argv[1:])
