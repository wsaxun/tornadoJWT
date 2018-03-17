# -*- coding: utf-8 -*-

from tornado.web import RequestHandler
from tornado.gen import coroutine
from api.handle.mixin import (RestfulMixin, CreateSessionMixin, OperationMixin)
from api.device.common import CheckParams
from data.models import Product
from util.exception import AppException


class Products(OperationMixin, CheckParams, CreateSessionMixin, RestfulMixin, RequestHandler):
    """
    产品添加、展示
    前端传递数据：
        {action: add/query, type: product, data:[{name: x,
        description: x}, {name: x,}
        ]}
    """

    @coroutine
    def post(self):
        if not self._check_params():
            raise AppException(ret_msg='missing some parameters')

        if self.request_body['type'] == 'product' and self.request_body[
            'action'] == 'add':
            try:
                for items in self.request_body['data']:
                    products = Product(**items)
                    self.sessions.add(products)
                    self.sessions.commit()
            except Exception as e:
                raise AppException(
                    ret_msg='failed, exception: %s' % e.__str__())
            self.jsonify(ret_msg=u"success")

        if self.request_body['type'] == 'product' and self.request_body[
            'action'] == 'query':
            result = []
            if isinstance(self.request_body['data'], unicode):
                for items in self.sessions.query(Product).all():
                    result.append({'f_id': items.f_id, 'f_name': items.f_name,
                                   'f_description': items.f_description})

            if isinstance(self.request_body['data'], list):
                for items in self.request_body['data']:
                    tmp = None
                    if items.has_key('f_id'):
                        tmp = self.sessions.query(Product).filter(
                            Product.f_id == int(items['f_id'])).one_or_none()

                    if items.has_key('f_name'):
                        tmp = self.sessions.query(Product).filter(
                            Product.f_name == items['f_name']).one_or_none()
                    if tmp:
                        result.append({'f_id': tmp.f_id,
                                       'f_name': tmp.f_name,
                                       'f_description': tmp.f_description})

            self.jsonify(ret_msg=u"success", data=result)

        if self.request_body['type'] == 'product':
            raise AppException(ret_msg=u'unsupported action')

        raise AppException(ret_msg=u'type error')