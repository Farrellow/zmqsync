# -*- coding: utf-8 -*-

import zmq

context = zmq.Context.instance()

class ZmqClient(object):
    def __init__(self, timeout):
        #server_url = 'inproc://server'                  # 线程间通信
        #server_url = 'ipc:///home/farrell/Study/zmq/1'  # 进程间通信
        server_url = 'tcp://127.0.0.1:9876'             # 不同主机进程间通信

        self.client = context.socket(zmq.REQ)
        self.client.setsockopt(zmq.LINGER, 2)
        self.client.connect(server_url)
        self.client.setsockopt(zmq.RCVTIMEO, timeout)

    def send_message(self, message):
        try:
            self.client.send(message)
            data = self.client.recv()
        except zmq.error.Again as e:
            print('zmq.error.Again: %s' % e)
            data = None
            err = e
        except zmq.error.ZMQError as e:
            print('zmq.error.ZMQError: %s' % e)
            data = None
            err = e
        else:
            # data handler
            print('data = %s' % data)
            err = None
        finally:
            return data, err

    def close(self):
        self.client.close()
