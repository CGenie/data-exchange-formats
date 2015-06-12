#!/usr/bin/env python

import socket

from pyasn1.codec.der import decoder
from pyasn1.codec.der import encoder
from pyasn1.type import univ

import chatroom


u = chatroom.User()
u.setComponentByName('id', univ.ObjectIdentifier((1, 1)))
u.setComponentByName('email', 'xyz@localhost')
u.setComponentByName('username', 'User')

rt = chatroom.RoomType()
rt.setComponentByName('public', None)

r = chatroom.Room()
r.setComponentByName('id', univ.ObjectIdentifier((2, 1)))
r.setComponentByName('name', 'Test Room')
r.setComponentByName('type', rt)

m = chatroom.Message()
m.setComponentByName('id', univ.ObjectIdentifier((3, 1)))
m.setComponentByName('user', u)
m.setComponentByName('room', r)
m.setComponentByName('message', 'Test chatroom message')


if __name__ == '__main__':
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect(('localhost', 8001))

    server.send(encoder.encode(m))
