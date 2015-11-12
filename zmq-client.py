#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
import zmq
import time
import random
from names import generate_name


context = zmq.Context()
# FRB prefix so it won't clash with auto generated variables of docker compose
server = os.environ.get("FRB_QUEUE_HOST", "localhost")
port = os.environ.get("FRB_CLIENT_PORT", "5559")

print "Connecting to server..."
socket = context.socket(zmq.REQ)
socket.connect("tcp://{}:{}".format(server, port))

client_id = generate_name()

poller = zmq.Poller()
poller.register(socket, zmq.POLLIN | zmq.POLLOUT)

colors = {
    'bold': '\033[1m',
    'red': '\033[31m',
    'yellow': '\033[33m',
    'green': '\033[32m',
    'blue': '\033[34m',
    'magenta': '\033[35m',
    'cyan': '\033[36m',
    'white': '\033[37m',
    'normal': '\033[0m',
}


def log(response):
    msg_template = (
        "{red}[CLIENT: {}]"
        "{bold}{green}SERVER "
        "{white}{} "
        "{magenta}{}{normal}"
    )
    print msg_template.format(client_id, response['server_id'], response['message'], **colors)


while True:
    available = dict(poller.poll())

    if socket not in available:
        continue

    if available[socket] == zmq.POLLOUT:
        request = {
            'client_id': client_id,
            'message': generate_name()
        }
        socket.send_json(request)

    if available[socket] == zmq.POLLIN:
        response = socket.recv_json()
        log(response)

    time.sleep(random.choice([.3, .5, .8, .2, .6]))
