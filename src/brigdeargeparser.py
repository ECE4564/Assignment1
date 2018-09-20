import argparse


def bridge_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('-brg', dest='bridge_ip',
                        help='Setting the bridge ip')

    parser.add_argument('-p', dest='bridge_port',
                        help='Setting the bridge port')

    parser.add_argument('-z', dest='socket_size',
                        help='Set the size of socket')

    parser.add_argument('-t', dest='hashtag',
                        help='Set the hashtag to listen to')

    parser.add_argument('--version', action='version', version='%(prog)s 1.0')

    return parser
