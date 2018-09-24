
from src.argparser import bridge_parser
from src.createSoc import connect, openPort
from src.hash import decodeMessage, unPickle, decryptMessage, encodeMessage, time
from src.ibmWatson import WatsonTextToSpeech

args = bridge_parser().parse_args()

server_port = int(args.server_port)
server_ip = args.server_ip
bridge_port = int(args.bridge_port)
backlog_size = int(args.backlog_size)
socket_size = int(args.socket_size)

watson = WatsonTextToSpeech()

serversocket = openPort(port=bridge_port, socket_size=socket_size)
#[ Checkpoint  01]  Created  socket  at  0.0.0.0  on  port <BRIDGE_PORT>
print(time() + "[Checkpoint 01] Created socket at 0.0.0.0  on  port {0}".format(bridge_port))

# Wait for data from client
print(time() + "[Checkpoint 02] Listening  for  client connections")

client, address = serversocket.accept()
# [Checkpoint 03] Accepted client connection  from CLIENT_IP>  on  port <CLIENT_PORT>
print(time() + "[Checkpoint 03] Accepted client connection  from", address[0], 'on port', address[1])
while True:

    data = unPickle(client.recv(socket_size))
    # [ Checkpoint  04]  Received  data : <UNPICKLED RECEIVED DATA>
    print(time() + "[Checkpoint 04] Received data: ", data)

    data = decodeMessage(data)
    plaintext = decryptMessage(data[1], data[0])
    #plaintext = "How fast is light?"
    data = [123456]
    # [ Checkpoint  05]  Decrypt :  Key : <ENCRYPTION KEY> |  Plaintext <DECRYPTED QUESTOIN>
    print(time() + "[ Checkpoint  05]  Decrypt :  Key : ", data[0], " |  Plaintext ", plaintext)

    watson.playAudio(plaintext)
    # [ Checkpoint  06]  Speaking  Question  : <QUESTION>
    print(time() + "[ Checkpoint  06]  Speaking  Question  :", plaintext)

    socket = connect(ip=server_ip, port=server_port, backlog_size=backlog_size)
    # [ Checkpoint  07]  Connecting  to <SERVER IP>  on  port <SERVER PORT #>
    print(time() + "[ Checkpoint  07]  Connecting  to ", server_ip, "  on  port ", server_port)

    sending = encodeMessage(plaintext)
    socket.send(sending)
    # [ Checkpoint  08]  Sending  data : <PICKLED QUESTION PAYLOAD>
    print(time() + "[ Checkpoint  08]  Sending  data : ", sending)

    data = socket.recv(socket_size)
    # [ Checkpoint  09]  Received  data : <ANSWER PAYLOAD>
    print(time() + "[ Checkpoint  09]  Received  data : ", data)

    data = decodeMessage(unPickle(data))
    print(data)
    plaintext = decryptMessage(data[1], data[0])
    # [ Checkpoint  10]  Decrypt :  Using Key : <ENCRYPTION KEY>|  Plaintext : <DECRYPTED ANSWER>
    print(time() + "[ Checkpoint  10]  Decrypt :  Using Key : ", data[0], "|  Plaintext :", plaintext)

    watson.playAudio(plaintext)
    # [ Checkpoint  11]  Speaking Answer  : <ANSWER>
    print(time() + "[ Checkpoint  11]  Speaking Answer  : ", plaintext)


#Command line interface - Done
'''
python3 bridge.py –svr-p <SERVER_PORT> -svr<SERVER_IP_ADDR> -p <BRIDGE_PORT> -b <BACKLOG_SIZE> -z <SOCKET_SIZE>
'''
