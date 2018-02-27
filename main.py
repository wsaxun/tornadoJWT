# -*- coding: utf-8 -*-

import sys
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
    app = make_app(routers)    
    setattr(app, u'options', options)
    setattr(app, u'sessions', sessions)
    app.listen(port=options.port, address=options.bind)
    try:
        IOLoop.current().start()
    except Exception:
        IOLoop.current().stop()

if __name__ == u'__main__':
    main()
