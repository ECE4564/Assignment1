import socket

def connect(ip, port, backlog_size):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((ip, port))
    s.listen(backlog_size)
    return s

def openPort(port, socket_size):
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind((socket.gethostname(), port) )
    serversocket.listen(socket_size)
    return serversocket

from _thread import *
import threading

class ThreadedSocket:
    def __init__(self):


class ThreadedPort:
    def __init__(self):