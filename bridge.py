
from src.brigdeargeparser import bridge_parser

args = bridge_parser().parse_args()

bridge_ip = args.bridge_ip
bridge_port = args.bridge_port
socket_size = args.socket_size
hashtag = args.hashtag

#What the fuck does this need to do.

#Take question from client pass to server.
#Get answer from server
#Give that shit to IBM WATSON
#Play the fucking sound


'''
Bridge Rpi
	•Initiated on command line with parameter of serverinfo
	•Receives and deconstructs question/answer payload
	•Verify checksum•Decrypt answer
	•Sends question/answer to IBM Watson via API call
	•Downloads question/answer audio from IBM Watson
	•Plays question/answer audio•Deletes local question/answer audio
'''

#Command line interface
'''
python3 bridge.py–svr-p <SERVER_PORT> -svr<SERVER_IP_ADDR> -p <BRIDGE_PORT> -b <BACKLOG_SIZE> -z <SOCKET_SIZE>
'''
