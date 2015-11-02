#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import zmq
from zmq.devices.monitoredqueuedevice import MonitoredQueue


def main():
    in_prefix = bytes('in')
    out_prefix = bytes('out')
    monitoringdevice = MonitoredQueue(zmq.XREP, zmq.XREQ, zmq.PUB, in_prefix, out_prefix)

    monitoringdevice.bind_in("tcp://127.0.0.1:5559")
    monitoringdevice.bind_out("tcp://127.0.0.1:5560")
    monitoringdevice.bind_mon("tcp://127.0.0.1:5570")

    monitoringdevice.setsockopt_in(zmq.RCVHWM, 1)
    monitoringdevice.setsockopt_out(zmq.SNDHWM, 1)
    monitoringdevice.start()

if __name__ == "__main__":
    main()
