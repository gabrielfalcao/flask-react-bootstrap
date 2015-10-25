#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import gevent
import gevent.monkey
gevent.monkey.patch_all()
from subprocess import Popen, PIPE, STDOUT
import logging
import coloredlogs
from datetime import datetime

from flask import Flask, render_template
from flask import send_from_directory
from flask.ext.socketio import SocketIO, send, emit

logger = logging.getLogger('flask-app')

web = Flask(__name__)
web.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(web)

coloredlogs.install(level=logging.DEBUG)


@web.route('/')
def index():
    return render_template('index.html')


@web.route('/dist/<path:path>')
def send_js(path):
    return send_from_directory('dist', path)


@socketio.on('hello')
def websocket_hello(data):
    logger.info('client connected %s: ', data)
    emit('ready', {'ready': datetime.utcnow().strftime('%B %d, %Y')})


@socketio.on('ping')
def websocket_console(data):
    logger.warning("DATA: %s", data)
    cmd = 'ping -t 10 {domain}'.format(**data)
    logger.info("requested %s", data)
    logger.error(cmd)

    process = Popen(cmd, stdout=PIPE, stderr=STDOUT, shell=True)
    emit('shell', {'clear': False, 'line': '{0}\n'.format(cmd)})

    while True:
        raw = process.stdout.readline()
        if not raw:
            break

        logger.info("SHELL: %s", unicode(raw, 'utf-8'))
        gevent.sleep(0)
        emit('shell', {'line': unicode(raw, 'utf-8')})
        gevent.sleep(0)


if __name__ == '__main__':
    socketio.run(web)
