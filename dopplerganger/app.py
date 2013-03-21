# -*- coding: utf-8 -*-
import os.path

import tornado.ioloop
import tornado.web

from dopplerganger.util import render_template


class IndexHandler(tornado.web.RequestHandler):
    """Provides the client."""
    def get(self):
        self.write(render_template('index.tmpl'))


#class


def get_application(ioloop=None):
    if ioloop is None:
        ioloop = tornado.ioloop.IOLoop.instance()

    static_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")

    application = tornado.web.Application([
        (r"/", IndexHandler),
        (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": static_path}),
    ])

    return application

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
