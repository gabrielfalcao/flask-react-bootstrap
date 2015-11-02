#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import time
import logging
import coloredlogs
import zmq

from names import generate_name

logger = logging.getLogger()
zmq_context = zmq.Context()


def main():
    coloredlogs.install(level=logging.INFO, show_hostname=False)

    publisher = zmq_context.socket(zmq.PUB)
    publisher.bind('tcp://0.0.0.0:8888')

    poller = zmq.Poller()
    poller.register(publisher, zmq.POLLOUT)
    logger.info("listening on tcp://0.0.0.0:8888")

    MAX = 200
    index = 0
    while True:
        if index > MAX:
            url = 'stop'
        else:
            url = generate_name()
            index += 1

        try:
            socks = dict(poller.poll(0.3))

            if publisher in socks and socks[publisher] == zmq.POLLOUT:
                logger.info("sending data %s", url)
                publisher.send(b" ".join([b'status', bytes(url)]))
                if url == 'stop':
                    break
                else:
                    time.sleep(.13)
        except KeyboardInterrupt:
            publisher.close()
            zmq_context.term()
            raise SystemExit


if __name__ == '__main__':
    main()
