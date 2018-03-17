# -*- coding: utf-8 -*-


from tornado.web import URLSpec
from api.handle.common import TestRequest, UnknownAPI, TestAuth
from api.user.user import *
from api.device.hardwares import *
from api.device.products import *
from api.device.prices import *
from api.device.hardwareTypes import *
from api.device.history import *
from views.pages import *

routers = [
    (r'/test', TestRequest),
    (r'/test/login', TestAuth),
    (r'/register', Register),
    (r'/api/user/login', UserLogin),
    (r'/api/user/group', UserGroupOPS),
    URLSpec(r'/api/user/code', UserCode, name="code"),
    (r'/api/user/logout', UserLogout),
    (r'/api/device/hardware', Hardwares),
    (r'/api/device/hardwaretype', HardwareTypes),
    (r'/api/device/price', Prices),
    (r'/api/device/product', Products),
    (r'/api/device/history', Historys),
    URLSpec(r'/', LoginView, name="login"),
    URLSpec(r'/main', MainView, name="index"),
    URLSpec(r'/hardware', HardwareView, name="hardware"),
    URLSpec(r'/hardwaretype', HardwareTypeView, name="hardwaretype"),
    URLSpec(r'/history', HistoryView, name="history"),
    URLSpec(r'/productschema', ProductSchemaView, name="productschema"),
    URLSpec(r'/price', PriceView, name="price"),
    URLSpec(r'/output', OutputView, name="output"),
    (r'.*', UnknownAPI),
]
