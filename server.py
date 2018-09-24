import wolframalpha
import socket,sys,getopt
from serverVariable import app_id
from cryptography.fernet import Fernet
from src.hash import md5IsValid, unPickle, encodeMessage, time
from src.argparser import server_parser

def queryWolfram(question):
    client = wolframalpha.Client(app_id)
    res = client.query(question)
    answer = next(res.results).text
    return answer

def parseCommandLine(argv):
    args = server_parser().parse_args()
    return (args.server_port,args.socket_size,args.backlog_size)


def decrypt(question,key):
    f = Fernet(key)
    decryptedQuestion = f.decrypt(question)
    return decryptedQuestion


def main(argv):

    serverPort,socketSize,backlogSize = parseCommandLine(argv)
    
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((socket.gethostname(),serverPort))
    #[ Checkpoint  01]  Created  socket  at  0.0.0.0  on  port <BRIDGE_PORT>
    print(time() + "Created socket at 0.0.0.0  on  port {0}".format(serverPort))
    s.listen(backlogSize)
    
    #[Checkpoint  02]  Listening for client connections
    print(time() + "Listening for client connections")
    
    
    
    while 1:
        
        client, address = s.accept()

        # [Checkpoint 03] Accepted client connection  from <CLIENT_IP> on port <CLIENT_PORT>
        print(time() + "Accepted client connection  from", address[0], 'on port', address[1])

        data = client.recv(socketSize)

        key,encryptedQuestion,checkSum = unPickle(data)
        # [ Checkpoint 04 ] Received data : <UNPICKLED RECEIVED DATA>
        print(time() + "Received data {","hash: ",checkSum,"question: ",encryptedQuestion,"key: ",key,"}")
        if data:
           
            if md5IsValid(encryptedQuestion,checkSum):
                decryptedQuestion = (decrypt(encryptedQuestion,key)).decode("utf-8")
                # [Checkpoint 05] Decrypt : Key : <ENCRYPTION KEY> | Plaintext <DECRYPTED QUESTOIN>
                print(time() + "Decrypt : Key :" ,key," | Plaintext", decryptedQuestion)
                
                # [ Checkpoint  06]  Sending question to Wolframalpha : <TWITTER_QUESTION>
                print(time() + "Sending question to Wolframalpha :", decryptedQuestion)

                ans = queryWolfram(decryptedQuestion)

                # [ Checkpoint  07]  Received answer from Wolframalpha : <WOLFRAM_ANSWER>
                print(time() + "Wolfram  Answer  :", ans)

                payload = encodeMessage(ans)

                # [Checkpoint 08] Encrypt : Key : <ENCRYPTION KEY> | Cipher text : <ENCRYPTED ANSWER>
                print(time() + "Encrypt : Key : ",payload[0]," | Cipher text : ",payload[1])
                #[ Checkpoint 09 ] Generated MD5 Checksum: <ANSWER CHECKSUM>
                print(time() + "Generated MD5 Checksum  :", payload[2])
                
                #[ Checkpoint 10 ] Sending answer : <ANSWER PAYLOAD>
                print(time() + "Sending answer :", payload)
                client.send(payload)

                # client.close()
            else:
                print("Invalid CheckSum")

if __name__ == '__main__':
    main(sys.argv[1:])
