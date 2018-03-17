# -*- coding: utf-8 -*-

from tornado.web import RequestHandler
from tornado.gen import coroutine
from api.handle.mixin import (RestfulMixin, CreateSessionMixin, OperationMixin)
from api.device.common import CheckParams
from data.models import Hardware
from util.exception import AppException


class Hardwares(OperationMixin, CheckParams, CreateSessionMixin, RestfulMixin,
                RequestHandler):
    """
    产品添加、展示
    前端传递数据：
        {action: add/query/update, type: hardware, data:[{name: x,
        description: x}, {name: x,}
        ]}
    """

    @coroutine
    def post(self):
        if not self._check_params():
            raise AppException(ret_msg='missing some parameters')

        if self.request_body['type'] == 'hardware' and self.request_body[
            'action'] == 'add':
            try:
                for items in self.request_body['data']:
                    products = Hardware(**items)
                    self.sessions.add(products)
                    self.sessions.commit()
            except Exception as e:
                raise AppException(
                    ret_msg='failed, exception: %s' % e.__str__())
            self.jsonify(ret_msg=u"success")

        if self.request_body['type'] == 'hardware' and self.request_body[
            'action'] == 'query':
            result = []
            if isinstance(self.request_body['data'], unicode):
                for items in self.sessions.query(Hardware).all():
                    result.append({'f_id': items.f_id, 'f_name': items.f_name,
                                   'f_type': items.f_type,
                                   'f_description': items.f_description})

            if isinstance(self.request_body['data'], list):
                for items in self.request_body['data']:
                    tmp = None
                    if items.has_key('f_id'):
                        tmp = self.sessions.query(Hardware).filter(
                            Hardware.f_id == int(
                                items['f_id'])).one_or_none()

                    if items.has_key('f_name') and not items.has_key('f_id'):
                        tmp = self.sessions.query(Hardware).filter(
                            Hardware.f_name == items[
                                'f_name']).one_or_none()

                    if items.has_key('f_type') and not items.has_key(
                            'f_id') and not items.has_key('f_name'):
                        tmp = self.sessions.query(Hardware).filter(
                            Hardware.f_type == items['f_type']
                        ).all()

                    if tmp:
                        if isinstance(tmp, list):
                            try:
                                for db_result in tmp:
                                    result.append({'f_id': db_result.f_id,
                                                   'f_name': db_result.f_name,
                                                   'f_type': db_result.f_type,
                                                   'f_description': db_result.f_description})
                            except Exception as e:
                                raise AppException(
                                    ret_msg="failed exception: %s" % e.__str__())
                        else:
                            try:
                                result.append({'f_id': tmp.f_id,
                                               'f_name': tmp.f_name,
                                               'f_type': tmp.f_type,
                                               'f_description': tmp.f_description})
                            except Exception as e:
                                raise AppException(
                                    ret_msg="failed exception: %s" % e.__str__())

            self.jsonify(ret_msg=u"success", data=result)

        if self.request_body['type'] == 'hardware' and self.request_body[
            'action'] == 'update':
            querys = self.sessions.query(Hardware)
            if isinstance(self.request_body['data'], list):
                sql = {}
                try:
                    for items in self.request_body['data']:
                        if items.has_key('f_name'):
                            sql.update({Hardware.f_name: items['f_name']})
                        if items.has_key('f_type'):
                            sql.update({Hardware.f_type: items['f_type']})
                        if items.has_key('f_description'):
                            sql.update({Hardware.f_description: items['f_description']})
                        querys.filter(Hardware.f_id == items['f_id']).update(sql)
                        self.sessions.commit()
                except Exception as e:
                    raise AppException(
                        ret_msg="failed, exception: %s" % e.__str__())

                self.jsonify(ret_msg='success')
