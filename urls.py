# -*- coding: utf-8 -*-


from api.handle.common import TestRequest, UnknownAPI, TestAuth
from api.user.user import *
from tornado.web import URLSpec

routers = [
    (r'/test', TestRequest),
    (r'/test/login',TestAuth),
    (r'/register', Register),
    (r'/api/user/login', UserLogin),
    (r'/api/user/group', UserGroupOPS),
    URLSpec(r'/api/user/code', UserCode, name="code"),
    (r'/api/user/logout', UserLogout),
    (r'.*', UnknownAPI),
]

