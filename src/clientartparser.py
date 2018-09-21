import argparse


def client_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('-brg', dest='bridge_ip',
                        help='Bridge IP address')

    parser.add_argument('-p', dest='bridge_port',
                        help='Bridge port')

    parser.add_argument('-z', dest='socket_size',
                        help='Set the size of socket')

    parser.add_argument('-t', dest='hash_tag',
                        help='Set the HASH TAG we are looking for')

    parser.add_argument('--version', action='version', version='%(prog)s 6.9')

    return parser
