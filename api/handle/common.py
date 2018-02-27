# -*- coding: utf-8 -*-

from tornado.web import RequestHandler
from tornado.gen import coroutine
from data.models import *
from util.sourcePools import ExecutorPoolFactory
from util.exception import AppException
from mixin import RestfulMixin, CreateSessionMixin, OperationMixin


class TestRequest(RestfulMixin, CreateSessionMixin, RequestHandler):
    def _db_operation(self):
        return self.sessions.query(User.f_user, User.f_passwd)

    @coroutine
    def get(self):
        self.access_control_allow()
        data = []
        result = yield ExecutorPoolFactory.create_pool('io').submit(
            self._db_operation)
        for user, passwd in result:
            data.append({'user': user, 'passwd': passwd})
        self.jsonify(ret_msg=u"success", data=data)

    @coroutine
    def post(self):
        self.access_control_allow()
        self.jsonify(ret_msg=u"success", data=[3, 2, 1])


class TestAuth(RestfulMixin, OperationMixin, RequestHandler):
    def _db_operation(self):
        return self.sessions.query(User.f_user, User.f_passwd)

    @coroutine
    def get(self):
        self.access_control_allow()
        data = []
        result = yield ExecutorPoolFactory.create_pool('io').submit(
            self._db_operation)
        for user, passwd in result:
            data.append({'user': user, 'passwd': passwd})
        self.jsonify(ret_msg=u"success", data=data)

    @coroutine
    def post(self):
        self.access_control_allow()
        self.jsonify(ret_msg=u"success", data=[3, 2, 1])


class UnknownAPI(RestfulMixin, RequestHandler):
    @coroutine
    def get(self):
        self.access_control_allow()
        raise AppException(500, ret_msg=u"unknown api")

    @coroutine
    def post(self):
        self.access_control_allow()
        raise AppException(500, ret_msg=u"unknown api")
