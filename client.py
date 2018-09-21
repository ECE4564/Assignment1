from src.clientargparser import client_parser

args = client_parser().parse_args()

bridge_ip = args.bridge_ip
bridge_port = args.bridge_port
socket_size = args.socket_size
hash_tag = args.hash_tag

print(bridge_ip, bridge_port, socket_size, hash_tag)
