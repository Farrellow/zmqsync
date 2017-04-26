# -*- coding: utf-8 -*-

from zmq_server import ZmqServer

if __name__ == '__main__':
    server = ZmqServer(4)
    server.start()
