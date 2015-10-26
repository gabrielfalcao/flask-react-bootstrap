#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
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
    emit('zeromq', b'---------\nconnected\n---------\n')
    gevent.sleep(0)


@socketio.on('zeromq')
def websocket_zeromq(*args, **kwargs):
    report_printer = zmq_context.socket(zmq.SUB)
    report_printer.setsockopt(zmq.SUBSCRIBE, b'status')
    report_printer.connect('tcp://0.0.0.0:8888')

    poller = zmq.Poller()
    poller.register(report_printer, zmq.POLLIN)

    logging.getLogger("requests").setLevel(logging.WARNING)
    logger.info('listening to zeromq on 0.0.0.0:8888')
    running = True
    while running:
        socks = dict(poller.poll(0.5))
        if report_printer in socks and socks[report_printer] == zmq.POLLIN:
            data = report_printer.recv()
            running = 'stop' not in data.lower()
            topic, value = data.split(' ', 1)
            gevent.sleep(0)
            emit('zeromq', "{0}\n".format(value))
            gevent.sleep(0)


@socketio.on('publisher_spawn')
def websocket_console(*data, **kw):
    logger.info("Client asked for publisher: %s", data)
    cmd = 'python publisher.py'

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
    socketio.run(web)
