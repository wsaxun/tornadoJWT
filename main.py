# -*- coding: utf-8 -*-

import sys
import os
from tornado.ioloop import IOLoop
from tornado.options import options, define
from application import make_app
from urls import routers
from util.dbSession import sessions

reload(sys)
sys.setdefaultencoding('utf8')


def main():
    define(u"port", default=80, help=u"server port", type=int)
    define(u"bind", default=u'0.0.0.0', help=u"server address", type=str)
    options.parse_command_line()
    settings = dict(
        template_path = os.path.join(os.path.dirname(__file__), "templates"),
        static_path =  os.path.join(os.path.dirname(__file__), "static")
    )
    app = make_app(routers, **settings)
    setattr(app, u'options', options)
    setattr(app, u'sessions', sessions)
    app.listen(port=options.port, address=options.bind)
    try:
        IOLoop.current().start()
    except Exception:
        IOLoop.current().stop()

if __name__ == u'__main__':
    main()
