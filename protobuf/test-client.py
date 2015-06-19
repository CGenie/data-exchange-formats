#!/usr/bin/env python

import base64
import socket
import sys

from compiled import chatroom_pb2
from compiled_v2 import chatroom_2_pb2


def v1_message():
    room_type = chatroom_pb2.PUBLIC

    message = chatroom_pb2.Message()
    message.id = 3
    message.user.id = 1
    message.user.email = 'user@example.com'
    message.user.username = 'test-user'

    message.room.id = 2
    message.room.name = 'test room'
    message.room.type = room_type

    message.msg = 'test message'

    print 'Serialized message: %r' % message.SerializeToString()
    print 'Base64-encoded: %s' % base64.b64encode(message.SerializeToString())

    return message


def v2_message():
    room_type = chatroom_2_pb2.PUBLIC

    message = chatroom_2_pb2.Message()
    message.id = 3
    message.user.id = 1
    message.user.email = 'user@example.com'
    message.user.username = 'test-user'
    message.user.first_name = 'Frank'
    message.user.last_name = 'Underwood'
    message.user.age = 50
    message.user.badges.extend(['novice', 'intermediate'])

    message.room.id = 2
    message.room.name = 'test room'
    message.room.type = room_type

    message.msg = 'test message'

    print 'Serialized message: %r' % message.SerializeToString()
    print 'Base64-encoded: %s' % base64.b64encode(message.SerializeToString())

    return message

if __name__ == '__main__':
    v_msg = v1_message
    version = 1
    if len(sys.argv) > 1 and sys.argv[1] == 'v2':
        v_msg = v2_message
        version = 2

    print 'Client version {}'.format(version)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect(('localhost', 8002))
    server.send(base64.b64encode(v_msg().SerializeToString()))

