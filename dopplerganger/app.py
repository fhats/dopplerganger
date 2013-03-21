# -*- coding: utf-8 -*-
import errno
import fcntl
from functools import partial
import json
import os.path
import socket

import tornado.ioloop
import tornado.iostream
import tornado.web

import dopplerganger.websocket
from dopplerganger.util import render_template
"""Takes messages of the format:

x\ty

and produces websocket messages with a format:

{
    x: x
    y: y
}
"""

class IndexHandler(tornado.web.RequestHandler):
    """Provides the client."""
    def get(self):
        self.write(render_template('index.tmpl'))


class SomeWebSocket(dopplerganger.websocket.WebSocketHandler):
    """What am I doing"""
    def open(self):
        def cb(x, y):
            self.write_point(x, y)
            self.application.settings['dm'].register_cb(cb)
        self.application.settings['dm'].register_cb(cb)
        self.write_message("bando shibbays")

    def on_message(self, message):
        self.write_message(message)

    def write_point(self, x, y):
        self.write_message(json.dumps({
            "x": x,
            "y": y
        }))


class IncomingDataManager(object):
    """Wat"""

    def __init__(self, ioloop, incoming_port):
        self.ioloop = ioloop
        self.incoming_port = incoming_port
        self.streams = []
        self.cb = []

    def start(self):
        self.prepare_socket(self.incoming_port)
        self.prepare_stream()

    def prepare_socket(self, incoming_port):
        """Server Socket Setup"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        flags = fcntl.fcntl(sock.fileno(), fcntl.F_GETFD)
        flags |= fcntl.FD_CLOEXEC
        fcntl.fcntl(sock.fileno(), fcntl.F_SETFD, flags)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setblocking(0)
        sock.bind(('0.0.0.0', incoming_port))
        sock.listen(128)
        self.sock = sock

    def prepare_stream(self):
        self.ioloop.add_handler(self.sock.fileno(), self.accept, tornado.ioloop.IOLoop.READ)

    def accept(self, fd, events):
        """Accept new incoming connection from a persistent client"""
        while True:
            try:
                connection, address = self.sock.accept()
            except socket.error, e:
                if e[0] in (errno.EWOULDBLOCK, errno.EAGAIN):
                    return
                else:
                    raise

            stream = tornado.iostream.IOStream(connection, io_loop=self.ioloop)
            connection.setblocking(0)

            self.read_stream(stream)

    def read_stream(self, stream):
        stream.read_until("\n", partial(self.stream_cb, stream=stream))

    def stream_cb(self, data, stream):
        data = data.strip()
        try:
            x,y = data.split("\t")
            self.pump_event(x, y)
        except:
            pass
        finally:
            self.read_stream(stream)

    def register_cb(self, cb):
        """Use me"""
        self.cb.append(cb)

    def pump_event(self, x, y):
        old_cbs = self.cb
        self.cb = []
        for cb in old_cbs:
            cb(x, y)


def get_application(incoming_port, ioloop=None):
    if ioloop is None:
        ioloop = tornado.ioloop.IOLoop.instance()

    dm = IncomingDataManager(ioloop, incoming_port)
    dm.start()

    static_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
    application = tornado.web.Application([
        (r"/", IndexHandler),
        (r"/oh-dear", SomeWebSocket),
        (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": static_path}),
    ], dm=dm)

    return application

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
