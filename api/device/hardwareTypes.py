# -*- coding: utf-8 -*-

from tornado.web import RequestHandler
from tornado.gen import coroutine
from api.handle.mixin import (RestfulMixin, CreateSessionMixin, OperationMixin)
from api.device.common import CheckParams
from data.models import HardwareType
from util.exception import AppException


class HardwareTypes(OperationMixin, CheckParams, CreateSessionMixin, RestfulMixin,
                    RequestHandler):
    """
    产品添加、展示
    前端传递数据：
        {token: x, action: add/query/update, type: hardwaretype, data:[{name: x,
        description: x}, {name: x,}
        ]}
    """

    @coroutine
    def post(self):
        if not self._check_params():
            raise AppException(ret_msg='missing some parameters')

        if self.request_body['type'] == 'hardwaretype' and self.request_body[
            'action'] == 'add':
            try:
                for items in self.request_body['data']:
                    products = HardwareType(**items)
                    self.sessions.add(products)
                    self.sessions.commit()
            except Exception as e:
                raise AppException(
                    ret_msg='failed, exception: %s' % e.__str__())
            self.jsonify(ret_msg=u"success")

        if self.request_body['type'] == 'hardwaretype' and self.request_body[
            'action'] == 'query':
            result = []
            if isinstance(self.request_body['data'], unicode):
                for items in self.sessions.query(HardwareType).all():
                    result.append({'f_id': items.f_id, 'f_name': items.f_name,
                                   'f_description': items.f_description})

            if isinstance(self.request_body['data'], list):
                for items in self.request_body['data']:
                    tmp = None
                    if items.has_key('f_id'):
                        tmp = self.sessions.query(HardwareType).filter(
                            HardwareType.f_id == int(
                                items['f_id'])).one_or_none()

                    if items.has_key('f_name') and not items.has_key('f_id'):
                        tmp = self.sessions.query(HardwareType).filter(
                            HardwareType.f_name == items[
                                'f_name']).one_or_none()
                    if tmp:
                        try:
                            result.append({'f_id': tmp.f_id,
                                           'f_name': tmp.f_name,
                                           'f_description': tmp.f_description})
                        except Exception as e:
                            raise AppException(
                                ret_msg="failed exception: %s" % e.__str__())

            self.jsonify(ret_msg=u"success", data=result)

        if self.request_body['type'] == 'hardwaretype' and self.request_body[
            'action'] == 'update':
            querys = self.sessions.query(HardwareType)
            if isinstance(self.request_body['data'], list):
                sql = {}
                try:
                    for items in self.request_body['data']:
                        if items.has_key('f_name'):
                            sql.update({HardwareType.f_name: items['f_name']})
                        if items.has_key('f_description'):
                            sql.update({HardwareType.f_description: items['f_description']})
                        querys.filter(HardwareType.f_id == items['f_id']).update(sql)
                        self.sessions.commit()
                except Exception as e:
                    raise AppException(
                        ret_msg="failed, exception: %s" % e.__str__())
                self.jsonify(ret_msg='success')
            else:
                raise AppException(
                    ret_msg="failed, exception: data must be a object")

        if self.request_body['type'] == 'hardwaretype':
            raise AppException(ret_msg=u'unsupported action')

        raise AppException(ret_msg=u'type error')