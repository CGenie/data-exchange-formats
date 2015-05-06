#!/usr/bin/env python

import json
import jsonschema
import time

from pyasn1.codec.der import encoder
from pyasn1.type import univ

import chatroom


def prepare_asn1_message():
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

    return m


def prepare_dict_message():
    return {
        'id': '2.2',
        'user': {
            'id': '1.1',
            'email': 'abx@localhost',
            'username': 'TestUser',
        },
        'room': {
            'id': '2.1',
            'name': 'Test Room',
            'type': 'public',
        },
        'message': 'This is a test message',
    }


message_schema = {
    'type': 'object',
    'properties': {
        'user': {
            'type': 'object',
            'properties': {
                'id': {'type': 'string', 'minLength': 1},
                'email': {'type': 'string', 'minLength': 1, 'maxLength': 40},
                'username': {'type': 'string', 'minLength': 1, 'maxLength': 40},
            },
        },
        'room': {
            'type': 'object',
            'properties': {
                'id': {'type': 'string', 'minLength': 1},
                'name': {'type': 'string', 'minLength': 1, 'maxLength': 40},
                'type': {'type': 'string', 'enum': ['private', 'public']},
            },
        },
        'message': {'type': 'string', 'minLength': 1, 'maxLength': 128},
    },
}


if __name__ == '__main__':
    m = prepare_asn1_message()
    start = time.time()

    for x in xrange(1000):
        encoder.encode(m)

    print 'ASN1 time: %s' % (time.time() - start)

    m = prepare_dict_message()
    start = time.time()

    for x in xrange(1000):
        json.dumps(x)

    print 'JSON time: %s' % (time.time() - start)

    start = time.time()

    for x in xrange(1000):
        jsonschema.validate(m, message_schema)
        json.dumps(x)

    print 'JSON with schema validation time: %s' % (time.time() - start)
