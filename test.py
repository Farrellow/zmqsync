# -*- coding: utf-8 -*-

import zmq

from zmq_client import ZmqClient

if __name__ == '__main__':
    client = ZmqClient(2000)
    for _ in range(10):
        data, err = client.send_message(b'asdf')
        if type(err) is zmq.error.ZMQError:
            client.close()
            del client
            break
