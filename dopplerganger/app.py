# -*- coding: utf-8 -*-
import tornado.ioloop
import tornado.web

from dopplerganger.util import render_template


class IndexHandler(tornado.web.RequestHandler):
    """Provides the client."""
    def get(self):
        self.write(render_template('index.tmpl'))


def get_application(ioloop=None):
    if ioloop is None:
        ioloop = tornado.ioloop.IOLoop.instance()

    application = tornado.web.Application([
        (r"/", IndexHandler),
    ])

    return application

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
