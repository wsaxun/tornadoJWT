# -*- coding: utf-8 -*-


from tornado.web import Application


def make_app(router, **settings):
    app = Application(router, **settings)
    return app
