#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import json
import gevent
import gevent.monkey
gevent.monkey.patch_all()

import zmq.green as zmq
from subprocess import Popen, PIPE, STDOUT
import logging
import coloredlogs
from datetime import datetime

from flask import Flask, render_template
from flask import send_from_directory
from flask.ext.socketio import SocketIO, emit

logger = logging.getLogger('flask-app')

web = Flask(__name__)
web.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(web)

zmq_context = zmq.Context()


def parse_monitor(raw):
    topic, binary, _, msg = raw
    data = json.loads(msg)
    return {
        'topic': topic,
        'data': data
    }


@web.route('/')
def index():
    return render_template('index.html')


@web.route('/favicon.ico')
def favicon():
    return send_from_directory('styles', 'favicon.ico')


@web.route('/dist/<path:path>')
def send_js(path):
    return send_from_directory('dist', path)


@socketio.on('hello')
def websocket_hello(data):
    logger.info('client connected %s: ', data)
    emit('ready', {'ready': datetime.utcnow().strftime('%B %d, %Y')})
    gevent.sleep(0)
    if int(data.get('connection_attempt', 0)) == 0:
        emit('zeromq', b'Hey, this is a message coming from flask through socket.io\n')
        emit('zeromq', b'as acknowledgement that the client/server connection is healthy. Yay!\n')
    else:
        emit('zeromq', b'reconnected to server\n')

    gevent.sleep(0)


@socketio.on('zeromq')
def websocket_zeromq(*args, **kwargs):

    queue_host = os.environ.get("FRB_QUEUE_HOST", "localhost")
    monitor_port = os.environ.get("FRB_MONITOR_PORT", "5570")

    report_printer = zmq_context.socket(zmq.SUB)
    report_printer.setsockopt(zmq.SUBSCRIBE, b'')
    report_printer.connect('tcp://{}:{}'.format(queue_host, monitor_port))

    poller = zmq.Poller()
    poller.register(report_printer, zmq.POLLIN)

    logging.getLogger("requests").setLevel(logging.WARNING)
    logger.info('listening to zeromq on 0.0.0.0:8888')
    running = True
    while running:
        socks = dict(poller.poll(0.5))
        if report_printer in socks and socks[report_printer] == zmq.POLLIN:
            raw = report_printer.recv_multipart()
            try:
                data = parse_monitor(raw)
                emit('zeromq', data)
            except TypeError:
                data = None
                logger.exception("could not json decode %s", repr(raw))

            gevent.sleep(0)


@socketio.on('publisher_spawn')
def websocket_console(*data, **kw):
    logger.info("Client asked for publisher: %s", data)
    cmd = 'ping google.com'

    process = Popen(cmd, stdout=PIPE, stderr=STDOUT, shell=True)
    emit('shell', {'clear': True, 'line': '{0}\n'.format(cmd)})

    while True:
        raw = process.stdout.readline()
        if not raw:
            break

        gevent.sleep(0)
        emit('shell', {'line': unicode(raw, 'utf-8')})
        gevent.sleep(0)


if __name__ == '__main__':
    coloredlogs.install(level=logging.DEBUG, show_hostname=False)
    socketio.run(web, host='0.0.0.0')
