#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import logging
import signal
from yoctopuce.yocto_api import *
from yoctopuce.yocto_relay import *

yrelay = "prupellaRelay"
yerrormsg = YRefParam()
server_address = ('10.10.11.72', 9970)
# lvl 1-9 normal / >= 10 debug
loglevel = 10

if loglevel >= 10:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


def signal_handler(signal, frame):
    print 'You pressed Ctrl+C!'
    s.close()
    sys.exit(0)


def usage():
    scriptname = os.path.basename(sys.argv[0])
    print("Usage:")
    print(scriptname + ' [ ON | OFF ]')
    print('Example:')
    print(scriptname + ' OFF')
    sys.exit()


def yoctorelay(state):
    if state.upper() == 'OFF' or state == '0':
        logger.info('Switchting to state A/OFF')
        relay.set_state(YRelay.STATE_A)
    elif state.upper() == 'ON' or state == '1':
        logger.info('Switching to state B/ON')
        relay.set_state(YRelay.STATE_B)
    else:
        logger.info('Unknown command: %s' % state)


if YAPI.RegisterHub("10.10.11.72", yerrormsg) != YAPI.SUCCESS:
    sys.exit("init error" + yerrormsg.value)

relay = YRelay.FindRelay(yrelay + ".relay1")

# Create a TCP/IP socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to the port
logger.info('Starting up on %s port %s' % server_address)
s.bind(server_address)
# Listen for incoming connections
s.listen(1)

while True:
    signal.signal(signal.SIGINT, signal_handler)
    # Wait for a connection
    logger.info('Waiting for a connection...')
    conn, addr = s.accept()

    try:
        print('Connection from ', addr)
        while True:
            data = conn.recv(1024)
            if data:
                print data.rstrip()
                yoctorelay(data.rstrip())
            else:
                break
    finally:
        conn.close()
