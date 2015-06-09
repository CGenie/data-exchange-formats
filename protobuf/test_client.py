#!/usr/bin/env python

from compiled import chatroom_pb2

user = chatroom_pb2.User()
user.id = 1234
user.email = 'user@example.com'
user.username = 'test-user'

print 'Serialized user: %r' % user.SerializeToString()

