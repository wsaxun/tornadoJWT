# -*- coding: utf-8 -*-

import json
import urllib
from tornado.httpclient import AsyncHTTPClient
from tornado.gen import coroutine, Return
from util.exception import TokenException, AppException
from util.token import Token
from util.permission import Permission
from util.parseYaml import conf


class RestfulMixin(object):
    """ 设置必要的动作
    """

    def access_control_allow(self):
        # 允许 JS 跨域调用
        self.set_header(u"Access-Control-Allow-Methods", u"GET,POST")
        self.set_header(u"Access-Control-Allow-Headers",
                        u"Content-Type, Depth, User-Agent, X-File-Size, "
                        u"X-Requested-With, X-Requested-By, If-Modified-Since, "
                        u"X-File-Name, Cache-Control, Token")
        self.set_header(u'Access-Control-Allow-Origin', u'*')
        self.set_header(u'Content-Type', u'application/json; charset=UTF-8')

    def _write(self, args, **kwargs):
        result = {u'ret': args}
        result.update(kwargs)
        self.write(result)
        self.finish()

    def jsonify(self, args=0, **kwargs):
        if args == 0:
            self.set_status(200)
        else:
            self.set_status(args)
        self._write(args, **kwargs)

    def get(self, *args, **kwargs):
        self.access_control_allow()
        self.jsonify(405, ret_msg="method tot allowed")

    def write_error(self, args=500, **kwargs):
        self.set_status(args)
        excptions = kwargs['exc_info'][1]
        kwargs = excptions.kwargs
        self._write(args, **kwargs)


class SQLMixin(object):
    """ 连接数据库，关闭数据库连接
    """

    def make_session(self):
        self.sessions = self.application.sessions

    def close_session(self):
        self.sessions.close()


class AuthMixin(object):
    """ token验证身份
    """

    @coroutine
    def auth(self):
        if self.request.method == 'GET':
            raise Return(False)
        if not self.request.body:
            raise AppException(400, ret_msg="no token")
        body = json.loads(self.request.body)
        if not body.has_key('token'):
            raise AppException(400, ret_msg="no token")
        token = body['token']
        token_manager = Token()
        try:
            data = token_manager.detoken(token)
        except TokenException as e:
            raise AppException(500, ret_msg=e.message)
        self.token_data = data
        raise Return(True)


class PermissionMixin(Permission):
    """ request 验证权限
    """

    @coroutine
    def check_permission(self):
        result = yield self.permission()
        if not result:
            raise AppException(403, ret_msg="permission denied")
        raise Return(True)


class OperationMixin(AuthMixin, SQLMixin, PermissionMixin):
    """ requst准备session、token、清理session
    """

    @coroutine
    def prepare(self):
        self.make_session()
        status = yield self.auth()
        if status:
            yield self.check_permission()

    def on_finish(self):
        self.close_session()


class CreateSessionMixin(SQLMixin):
    """ request 准备session
    """

    def prepare(self):
        self.make_session()

    def on_finish(self):
        self.close_session()


class IpanelOAuth2Mixin(object):
    @coroutine
    def get_access_token(self):
        http = AsyncHTTPClient()
        body = urllib.urlencode({
            "oauth2_id": conf['ipanel']['oauth2_id'],
            "secret": conf['ipanel']['secret']
        })

        try:
            response = yield http.fetch(
                conf['ipanel']['access_token_url'] + '?' + body)
        except Exception as e:
            raise AppException(500,
                               ret_msg=u"ipanel access_token fail, exception： %s"
                                       % (e.message or e.strerror))
        raise Return(response.body)

    def get_user_code(self):
        try:
            code = self.get_argument('code')
        except Exception:
            raise AppException(500, ret_msg=u"ipanel code fail")
        return code

    @coroutine
    def get_user_info(self, access_token, code):
        http = AsyncHTTPClient()
        body = urllib.urlencode({
            'access_token': access_token,
            'code': code
        })
        try:
            response = yield http.fetch(
                conf['ipanel']['user_info_url'] + '?' + body)
        except Exception as e:
            raise AppException(500,
                               ret_msg=u'ipanle user info failed， exception： %s' % (
                               e.message or e.strerror))
        raise Return(response.body)
