# -*- coding: utf-8 -*-

import threading
import zmq

context = zmq.Context.instance()

class ZmqWorker(threading.Thread):
    def __init__(self, worker_url):
        threading.Thread.__init__(self)
        self.worker_url = worker_url

    def run(self):
        worker = context.socket(zmq.REP)
        worker.connect(self.worker_url)
        while True:
            message = worker.recv()
            # message handler
            print('message = %s' % message)
            worker.send(b';')

class ZmqServer(threading.Thread):
    def __init__(self, queue_count):
        threading.Thread.__init__(self)
        self.queue_count = queue_count

    def run(self):
        #server_url = 'inproc://server'                  # 线程间通信
        #server_url = 'ipc:///root/zmq/1'                # 进程间通信
        server_url = 'tcp://127.0.0.1:9876'             # 不同主机进程间通信

        worker_url = 'inproc://workers'                 # 线程间通信
        #worker_url = 'ipc:///root/zmq/0'               # 进程间通信
        #worker_url = 'tcp://192.168.14.208:9898'        # 不同主机进程间通信

        server = context.socket(zmq.ROUTER)
        server.bind(server_url)

        workers = context.socket(zmq.DEALER)
        workers.bind(worker_url)

        try:
            for _ in range(self.queue_count):
                worker_t = ZmqWorker(worker_url)
                worker_t.start()

            zmq.device(zmq.QUEUE, server, workers)
        except Exception as e:
            print('Exception: %s' % e)
        finally:
            server.close()
            workers.close()
            context.term()
