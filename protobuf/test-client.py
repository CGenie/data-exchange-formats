#!/usr/bin/env python

import base64
import socket

from compiled import chatroom_pb2
from compiled_v2 import chatroom_2_pb2


def v1_user():
    user = chatroom_pb2.User()
    user.id = 1234
    user.email = 'user@example.com'
    user.username = 'test-user'

    print 'Serialized user: %r' % user.SerializeToString()
    print 'Base64-encoded: %s' % base64.b64encode(user.SerializeToString())

    return user


def v2_user():
    user = chatroom_2_pb2.User()
    user.id = 1234
    user.email = 'user@example.com'
    user.username = 'test-user'
    user.first_name = 'Frank'
    user.last_name = 'Underwood'
    user.age = 50

    print 'Serialized user: %r' % user.SerializeToString()
    print 'Base64-encoded: %s' % base64.b64encode(user.SerializeToString())

    return user

if __name__ == '__main__':
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect(('localhost', 8002))
    server.send(base64.b64encode(v1_user().SerializeToString()))

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect(('localhost', 8002))
    server.send(base64.b64encode(v2_user().SerializeToString()))

