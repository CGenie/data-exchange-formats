#!/usr/bin/env python

import base64
import socket
import time
import traceback

from pyasn1.codec.ber import encoder as ber_encoder
from pyasn1.codec.der import decoder as der_decoder

import chatroom
import chatroom_v2


def decode(data, module):
    decoded = der_decoder.decode(data, module.Message())
    print decoded[0].prettyPrint()
    ber_encoded = ber_encoder.encode(decoded[0])
    # DER-encoded strings can be decoded with BER too
    print der_decoder.decode(ber_encoded, module.Message())[0].prettyPrint()
    with open('server-message-received', 'wb') as f:
        f.write(data)
    with open('server-message-received.b64', 'w') as f:
        f.write(base64.b64encode(data))


if __name__ == '__main__':
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 8001))
    server.listen(5)

    while 1:
        # accept connections from outside
        (clientsocket, address) = server.accept()

        data = clientsocket.recv(4096)

        print '-'*70

        print repr(data)
        try:
            decode(data, chatroom_v2)
        except:
            print 'Unsucessful V2 decoding, trying V1'
            try:
                decode(data, chatroom)
            except Exception:
                traceback.print_exc()
                print
        clientsocket.send('done')
