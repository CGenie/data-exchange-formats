#!/usr/bin/env python

import base64
import socket

from compiled import chatroom_pb2

user = chatroom_pb2.User()
user.id = 1234
user.email = 'user@example.com'
user.username = 'test-user'

print 'Serialized user: %r' % user.SerializeToString()
print 'Base64-encoded: %s' % base64.b64encode(user.SerializeToString())

if __name__ == '__main__':
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect(('localhost', 8002))

    server.send(base64.b64encode(user.SerializeToString()))

