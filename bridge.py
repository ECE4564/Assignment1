
from src.brigdeargeparser import bridge_parser
from src.createSocket import connect, openPort
from src.ibmWatson import WatsonTextToSpeech

import pickle

args = bridge_parser().parse_args()

server_port = int(args.server_port)
server_ip = args.server_ip
bridge_port = args.bridge_port
backlog_size = args.backlog_size
socket_size = args.socket_size

socket = connect(ip=server_ip, port=server_port, backlog_size=backlog_size)
serversocket = openPort(port=bridge_port, socket_size=socket_size)
watson = WatsonTextToSpeech()

while True:
    client1, address1 = socket.accept()
    print("Connected to server")
    client2, address2 = serversocket.accept()
    print("Client connected")
    data = client1.recv(socket_size)
    client2.send(data)
    data = pickle.loads(client2.recv(socket_size))
    stuff = watson.playAudio(data)
    #figure out how to play stuff


#What the fuck does this need to do.

#Take question from client pass to server.
#Get answer from server
#Give that shit to IBM WATSON
#Play the fucking sound


'''
Bridge Rpi
	•Initiated on command line with parameter of serverinfo - Done
	•Receives and deconstructs question/answer payload
	•Verify checksum
	•Decrypt answer
	•Sends question/answer to IBM Watson via API call
	•Downloads question/answer audio from IBM Watson
	•Plays question/answer audio•Deletes local question/answer audio
'''

#Command line interface - Done
'''
python3 bridge.py–svr-p <SERVER_PORT> -svr<SERVER_IP_ADDR> -p <BRIDGE_PORT> -b <BACKLOG_SIZE> -z <SOCKET_SIZE>
'''
