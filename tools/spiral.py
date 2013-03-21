#!/usr/bin/python
# -*- coding: utf-8 -*-
from optparse import OptionParser
import random
import socket


def connect_to(host, port):
    """Connects to host:port via TCP.

    Returns the resulting socket.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    return sock


def send_points(sock, x, y):
    message = "%d\t%d\n" % (x, y)
    sock.sendall(message)


def define_options():
    parser = OptionParser()
    parser.add_option('--host', default='127.0.0.1', help="Host")
    parser.add_option('-p', '--port', default=12345, type=int, help="Port")
    return parser


if __name__ == "__main__":
    parser = define_options()
    options, _ = parser.parse_args()

    sock = connect_to(options.host, options.port)

    for _ in xrange(50):
        x = random.randint(-1000, 1000)
        y = random.randint(-1000, 1000)
        send_points(sock, x, y)

    for x in xrange(960):
        for y in xrange(500):
            send_points(sock, x, y)

    sock.close()

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
