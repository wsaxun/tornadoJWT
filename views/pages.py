# -*- coding: utf-8 -*-


import urllib
from tornado.web import RequestHandler
from tornado.gen import coroutine
from api.user.user import UserCode
from api.handle.mixin import AuthMixin


class BaseAction(AuthMixin, UserCode):
    def get_user_code(self):
        pass

    @coroutine
    def action(self, name='main'):
        status = yield self.auth()
        if not status[0]:
            body = urllib.urlencode({
                'error': status[1].kwargs['ret_msg']
            })
            self.redirect(
                'http://' + self.request.host + self.application.reverse_url(
                    'login') + '?' + body)

        token = self.get_argument('token', None)
        if token:
            user = self.token_data['user']
            self.render("%s.html" %(name), user=user)
        else:
            body = urllib.urlencode({
                'error': u'not token'
            })
            self.redirect(
                'http://' + self.request.host + self.application.reverse_url(
                    'login') + '?' + body)


class LoginView(RequestHandler):
    @coroutine
    def get(self):
        msg = self.get_argument('error', default=None)
        self.render("login.html", error=msg)


class MainView(BaseAction):
    @coroutine
    def get(self):
        yield self.action('main')


class HardwareView(BaseAction):
    @coroutine
    def get(self):
        yield self.action('hardware')


class HardwareTypeView(BaseAction):
    @coroutine
    def get(self):
        yield self.action('hardwaretype')


class HistoryView(BaseAction):
    @coroutine
    def get(self):
        yield self.action('history')


class ProductSchemaView(BaseAction):
    @coroutine
    def get(self):
        yield self.action('productschema')


class PriceView(BaseAction):
    @coroutine
    def get(self):
        yield self.action('price')


class OutputView(BaseAction):
    @coroutine
    def get(self):
        yield self.action('output')