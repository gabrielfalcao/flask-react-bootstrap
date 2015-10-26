#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging
import itertools
import coloredlogs
import zmq

logger = logging.getLogger()
zmq_context = zmq.Context()


def main():
    coloredlogs.install(level=logging.INFO, show_hostname=False)

    publisher = zmq_context.socket(zmq.PUB)
    publisher.bind('tcp://0.0.0.0:8888')

    URLS = [
        'https://wordpress.com',
        'https://gnu.org',
        'http://httpbin.org/headers',
        'http://httpbin.org/get',
        'http://httpbin.org/json',
        'http://httpbin.org/json',
    ]
    poller = zmq.Poller()
    poller.register(publisher, zmq.POLLOUT)
    logger.info("listening on tcp://0.0.0.0:8888")

    MAX = 300
    for index, url in enumerate(itertools.cycle(URLS)):
        if index > MAX:
            url = 'stop'

        try:
            socks = dict(poller.poll(0.3))

            if publisher in socks and socks[publisher] == zmq.POLLOUT:
                logger.info("sending data %s", url)
                publisher.send(b" ".join([b'status', bytes(url)]))
                if url == 'stop':
                    break

        except KeyboardInterrupt:
            publisher.close()
            zmq_context.term()
            raise SystemExit


if __name__ == '__main__':
    main()
