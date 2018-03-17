# -*- coding: utf-8 -*-


import json
import urllib
from tornado.web import RequestHandler
from tornado.gen import coroutine, Return
from api.handle.mixin import (RestfulMixin, CreateSessionMixin, OperationMixin,
                              IpanelOAuth2Mixin)
from data.models import *
from util.sourcePools import ExecutorPoolFactory
from util.crypt import Crypt
from util.exception import AppException
from util.token import Token, TokenException
from util.parseYaml import conf


class Register(CreateSessionMixin, RestfulMixin, RequestHandler):
    def _db_operation(self, user_info):
        for info in user_info:
            users = User(f_user=info['user'], f_passwd=info['passwd'],
                         f_description=info['user'])
            self.sessions.add(users)
            self.sessions.commit()
            users_id = self.sessions.query(User.f_id).filter(
                User.f_user == info['user']).one()[0]
            group_id = self.sessions.query(UserGroup.f_id).filter(
                UserGroup.f_user_group == info['group'])
            groups = UserRelationGroup(f_user_id=users_id,
                                       f_user_group_id=group_id)
            self.sessions.add(groups)
            self.sessions.commit()

    @coroutine
    def post(self):
        self.access_control_allow()
        body = json.loads(self.request.body)
        if not body.has_key('data'):
            raise AppException(400, ret_msg=u'args error')

        user_info = []
        for info in body['data']:
            try:
                passwd = info['passwd']
                user = info['user']
                group = info['group']
            except KeyError:
                raise AppException(400, ret_msg=u'args error')
            if passwd is None:
                continue
            passwd = Crypt().encrypt(passwd)
            user_info.append({'user': user, 'passwd': passwd, 'group': group})

        if user_info:
            try:
                yield ExecutorPoolFactory.create_pool('io').submit(
                    self._db_operation,
                    user_info)
            except Exception as e:
                raise AppException(500, ret_msg=e.message)

        self.jsonify(ret_msg=u"success")


class UserLogin(CreateSessionMixin, RestfulMixin, RequestHandler):
    def _db_operation(self, user, passwd):
        status = self.sessions.query(User).filter(User.f_user == user,
                                                  User.f_passwd == passwd).count()
        return status

    @coroutine
    def get(self):
        body = urllib.urlencode({
            'oauth2_id': conf['ipanel']['oauth2_id'],
            'redirect_uri': 'http://' + self.request.host + self.application.reverse_url(
                'code'),
            'agentid': conf['ipanel']['agent_id'],
            'state': 'ipanel',
            'response_type': 'code',
            'scope': 'snsapi_base',
            'logout': '0'
        })
        self.redirect(conf['ipanel']['code_url'] + '?' + body)

    @coroutine
    def post(self):
        self.access_control_allow()
        try:
            user = self.get_argument('user')
            passwd = self.get_argument('passwd')
        except Exception:
            raise AppException(401, ret_msg=u'login failed')

        passwd = Crypt().encrypt(passwd)
        status = yield ExecutorPoolFactory.create_pool('io').submit(
            self._db_operation, user, passwd)
        if status:
            token_manager = Token()
            try:
                token = token_manager.entoken(user=user)
            except TokenException as e:
                raise AppException(500, ret_msg=e.message)
            self.jsonify(ret_msg=u'success', token=token)
            raise Return()
        raise AppException(401, ret_msg=u'login failed')


class UserGroupOPS(OperationMixin, RestfulMixin, RequestHandler):
    """ {type: usergroup, action: query, data: []}
    """

    @coroutine
    def post(self):
        self.access_control_allow()
        body = json.loads(self.request.body)
        try:
            types = body['type']
            action = body['action']
        except Exception:
            raise AppException(400, ret_msg=u'args error')
        if types == 'usergroup' and action == 'query':
            result = [group[0] for group in
                      self.sessions.query(UserGroup.f_user_group).all() if
                      group]
            self.jsonify(ret_msg="success", data=result)
            return

        raise AppException(400, ret_msg="unknown args")


class UserCode(IpanelOAuth2Mixin, RestfulMixin, RequestHandler):
    """ achieve user code
    """

    @coroutine
    def prepare(self):
        self.code = self.get_user_code()
        self.access_token = yield self.get_access_token()

    @coroutine
    def get(self):
        self.access_control_allow()
        user_info = yield self.get_user_info(
            json.loads(self.access_token)['access_token'], self.code)
        user_info = json.loads(user_info)
        if not user_info.has_key('user_id'):
            # raise AppException(500, ret_msg=user_info['ret_msg'])
            body = urllib.urlencode({
                'error': user_info['ret_msg']
            })
            self.redirect(
                'http://' + self.request.host + self.application.reverse_url(
                    'login') + '?' + body)

        token_manager = Token()
        try:
            token = token_manager.entoken(user=user_info['user_id'])
        except TokenException as e:
            body = urllib.urlencode({
                'error': e.message
            })
            self.redirect(
                'http://' + self.request.host + self.application.reverse_url(
                    'login') + '?' + body)
            # raise AppException(500, ret_msg=e.message)
            # self.jsonify(ret_msg=u'success', token=token, user=user_info['user_id'])
        body = urllib.urlencode({
            'token': token
        })
        self.redirect(
            'http://' + self.request.host + self.application.reverse_url(
                'index') + '?' + body)


class UserLogout(RestfulMixin, RequestHandler):
    @coroutine
    def get(self):
        body = urllib.urlencode({
            'oauth2_id': conf['ipanel']['oauth2_id'],
            'redirect_uri': 'http://' + self.request.host + '/',
            'agentid': conf['ipanel']['agent_id'],
            'state': 'ipanel',
            'response_type': 'code',
            'scope': 'snsapi_base',
            'logout': '1'
        })
        self.redirect(conf['ipanel']['code_url'] + '?' + body)

    @coroutine
    def post(self):
        self.get()
