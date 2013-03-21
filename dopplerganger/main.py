#!/usr/bin/python
# -*- coding: utf-8 -*-
from optparse import OptionParser

import tornado.httpserver
import tornado.ioloop

from dopplerganger.app import get_application


def run_app(port, ioloop=None):
    if not ioloop:
        ioloop = tornado.ioloop.IOLoop.instance()

    application = get_application(ioloop)

    http_server = tornado.httpserver.HTTPServer(application, io_loop=ioloop)
    http_server.listen(port)

    ioloop.start()


def define_options():
    parser = OptionParser()
    parser.add_option('-p', '--port', default=54321, type=int, help="Port to listen on")
    return parser


if __name__ == "__main__":
    parser = define_options()
    options, _ = parser.parse_args()

    run_app(options.port)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
