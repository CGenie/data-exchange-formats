#!/usr/bin/env python

import base64
import datetime
from dateutil import tz
import socket
import sys

from compiled import chatroom_pb2
from compiled_v2 import chatroom_2_pb2


utc = tz.gettz('UTC')


email = 'president@whitehouse.gov'
username = 'MrPresident'
first_name = 'Frank'
last_name = 'Underwood'
age = 50
roomname = 'Chat with Claire'
message_text = 'Hello Honey'


def v1_message():
    room_type = chatroom_pb2.PUBLIC

    message = chatroom_pb2.Message()
    message.id = 3
    message.user.id = 1
    message.user.email = email
    message.user.username = username

    message.room.id = 2
    message.room.name = roomname
    message.room.type = room_type

    message.timestamp = datetime.datetime.now(tz=utc).isoformat()

    message.msg = message_text

    print 'Serialized message: %r' % message.SerializeToString()
    print 'Base64-encoded: %s' % base64.b64encode(message.SerializeToString())

    return message


def v2_message():
    room_type = chatroom_2_pb2.PUBLIC

    message = chatroom_2_pb2.Message()
    message.id = 3
    message.user.id = 1
    message.user.email = email
    message.user.username = username
    message.user.first_name = first_name
    message.user.last_name = last_name
    message.user.age = age
    message.user.badges.extend(['caring', 'loving'])

    message.room.id = 2
    message.room.name = roomname
    message.room.type = room_type

    message.timestamp = datetime.datetime.now(tz=utc).isoformat()

    message.msg = message_text

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

