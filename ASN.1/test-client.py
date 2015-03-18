#!/usr/bin/env python

import socket

from pyasn1.codec.der import decoder
from pyasn1.codec.der import encoder

import weapons


q = weapons.FooQuestion()
q.setComponentByName('trackingNumber', 5)
q.setComponentByName('question', 'How are you?')


if __name__ == '__main__':
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 8001))

    client.send(encoder.encode(q))
