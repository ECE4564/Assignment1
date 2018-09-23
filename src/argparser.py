import argparse

def bridge_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('-svr-p', dest='server_port',
                        help='Setting the server_port')

    parser.add_argument('-svr', dest='server_ip',
                        help='Setting the server ip')

    parser.add_argument('-p', dest='bridge_port',
                        help='Setting the bridge port')

    parser.add_argument('-b', dest='backlog_size',
                        help='Set the size of backlog')

    parser.add_argument('-z', dest='socket_size',
                        help='Set the size of socket')

    parser.add_argument('--version', action='version', version='%(prog)s 1.0')

    return parser


def server_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('-p', dest='server_port',
                        help='Setting the server_port')

    parser.add_argument('-b', dest='backlog_size',
                        help='Set the size of backlog')

    parser.add_argument('-z', dest='socket_size',
                        help='Set the size of socket')
    return parser