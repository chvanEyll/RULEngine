#Under MIT License, see LICENSE.txt
#!/usr/bin/python

from socketserver import ThreadingMixIn, UDPServer, BaseRequestHandler
import threading
import socket
import struct
from collections import deque
import pickle


def getUDPHandler(packet_list):
    class ThreadedUDPRequestHandler(BaseRequestHandler):

        def handle(self):
            data = self.request[0]
            packet_list.append(pickle.loads(data))

    return ThreadedUDPRequestHandler


class UIDebugPacketReceiver(ThreadingMixIn, UDPServer):

    allow_reuse_address = True

    def __init__(self, host, port):
        self.packet_list = deque(maxlen=100)
        handler = getUDPHandler(self.packet_list)
        super(UIDebugPacketReceiver, self).__init__((host, port), handler)
        server_thread = threading.Thread(target=self.serve_forever)
        server_thread.daemon = True
        server_thread.start()

    def pop_frames(self):
        new_list = list(self.packet_list)
        self.packet_list.clear()
        return new_list

    def get_latest_frame(self):
        try:
            return self.packet_list[-1]
        except IndexError:
            return None
