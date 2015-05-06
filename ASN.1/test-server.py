#!/usr/bin/env python

import base64
import socket
import time
import traceback

from pyasn1.codec.der import decoder
from pyasn1.codec.der import encoder

import chatroom


if __name__ == '__main__':
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 8001))
    server.listen(5)

    while 1:
        #accept connections from outside
        (clientsocket, address) = server.accept()
        #now do something with the clientsocket
        #in this case, we'll pretend this is a threaded server
        #ct = client_thread(clientsocket)
        #ct.run()
        data = clientsocket.recv(4096)
        print data
        try:
            decoded = decoder.decode(data, chatroom.Message())
            print decoded[0].prettyPrint()
            with open('server-message-received', 'wb') as f:
                f.write(data)
            with open('server-message-received.b64', 'w') as f:
                f.write(base64.b64encode(data))
        except Exception:
            traceback.print_exc()
            print
        time.sleep(1)
