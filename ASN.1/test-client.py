#!/usr/bin/env python

import datetime
from dateutil import tz
import socket
import sys

from pyasn1.codec.der import encoder
from pyasn1.type import univ, useful

import chatroom
import chatroom_v2


utc = tz.gettz('UTC')

email = 'president@whitehouse.gov'
username = 'MrPresident'
first_name = 'Frank'
last_name = 'Underwood'
age = 50
roomname = 'Chat with Claire'
now = datetime.datetime.now(tz=utc)
now_s = useful.UTCTime(now.strftime('%y%m%d%H%M%S'))
message = 'Hello Honey'


def v1_message():
    u = chatroom.User()
    u.setComponentByName('id', univ.ObjectIdentifier((1, 1)))
    u.setComponentByName('email', email)
    u.setComponentByName('username', username)

    rt = chatroom.RoomType()
    rt.setComponentByName('private', None)

    r = chatroom.Room()
    r.setComponentByName('id', univ.ObjectIdentifier((2, 1)))
    r.setComponentByName('name', roomname)
    r.setComponentByName('type', rt)

    m = chatroom.Message()
    m.setComponentByName('id', univ.ObjectIdentifier((2, 2)))
    m.setComponentByName('user', u)
    m.setComponentByName('room', r)
    m.setComponentByName('timestamp', now_s)
    m.setComponentByName('message', message)

    return m


def v2_message():
    u = chatroom_v2.User()
    u.setComponentByName('id', univ.ObjectIdentifier((1, 1)))
    u.setComponentByName('email', email)
    u.setComponentByName('username', username)
    u.setComponentByName('firstName', first_name)
    u.setComponentByName('lastName', last_name)
    u.setComponentByName('age', age)
    badges_idx = u.componentType.getPositionByName('badges')
    badges_tt = u.componentType.getTypeByPosition(badges_idx).clone()
    badges_tt[0] = 'caring'
    badges_tt[1] = 'loving'
    u.setComponentByName('badges', badges_tt)
    u.setComponentByName('afterBadges', 'after badges')

    rt = chatroom_v2.RoomType()
    rt.setComponentByName('private', None)

    r = chatroom_v2.Room()
    r.setComponentByName('id', univ.ObjectIdentifier((2, 1)))
    r.setComponentByName('name', roomname)
    r.setComponentByName('type', rt)

    m = chatroom_v2.Message()
    m.setComponentByName('id', univ.ObjectIdentifier((2, 1)))
    m.setComponentByName('user', u)
    m.setComponentByName('room', r)
    m.setComponentByName('timestamp', now_s)
    m.setComponentByName('message', message)

    return m


if __name__ == '__main__':
    v_msg = v1_message
    version = 1
    if len(sys.argv) > 1 and sys.argv[1] == 'v2':
        v_msg = v2_message
        version = 2

    print 'Running in version {}'.format(version)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.connect(('localhost', 8001))
    server.send(encoder.encode(v_msg()))
    print server.recv(4096)
