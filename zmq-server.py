#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import os
import time

import zmq

from names import generate_name

# FRB prefix so it won't clash with auto generated variables of docker compose
queue_host = os.environ.get("FRB_QUEUE_HOST", "localhost")
port = os.environ.get("FRB_SERVER_PORT", "5560")

context = zmq.Context()
socket = context.socket(zmq.REP)
connection = "tcp://{}:{}".format(queue_host, port)
print 'connection', connection, queue_host, port
socket.connect(connection)
server_id = generate_name()

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


def log(request):
    msg_template = (
        "{red}[SERVER: {}]"
        "{bold}{red}CLIENT "
        "{yellow}{} "
        "{blue}{}{normal}"
    )
    print msg_template.format(server_id, request['client_id'], request['message'], **colors)


while True:
    available = dict(poller.poll())
    time.sleep(.3)

    if socket not in available:
        continue

    if available[socket] == zmq.POLLOUT:
        response = {
            'server_id': server_id,
            'message': generate_name()
        }
        socket.send_json(response)

    if available[socket] == zmq.POLLIN:
        request = socket.recv_json()
        log(request)
