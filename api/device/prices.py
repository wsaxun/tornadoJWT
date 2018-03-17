# -*- coding: utf-8 -*-

from tornado.web import RequestHandler
from tornado.gen import coroutine
from api.handle.mixin import (RestfulMixin, CreateSessionMixin, OperationMixin)
from api.device.common import CheckParams
from data.models import Price, Hardware
from util.exception import AppException


class Prices(OperationMixin, CheckParams, CreateSessionMixin, RestfulMixin,
             RequestHandler):
    """
    产品添加、展示
    前端传递数据：
        {token: x, action: add/query/update, type: price, data:[{name: x,
        description: x}, {name: x,}
        ]}
    """

    @coroutine
    def post(self):
        if not self._check_params():
            raise AppException(ret_msg='missing some parameters')

        if self.request_body['type'] == 'price' and self.request_body[
            'action'] == 'add':
            try:
                for items in self.request_body['data']:
                    products = Price(**items)
                    self.sessions.add(products)
                    self.sessions.commit()
            except Exception as e:
                raise AppException(
                    ret_msg='failed, exception: %s' % e.__str__())
            self.jsonify(ret_msg=u"success")

        if self.request_body['type'] == 'price' and self.request_body[
            'action'] == 'query':
            result = []
            if isinstance(self.request_body['data'], unicode):
                for items in self.sessions.execute("select h.f_id as f_h_id, h.f_name, p.f_id,"
                                                   "p.f_business_price, "
                                                   "p.f_cost_price, "
                                                   "p.f_description from t_hardware h "
                                                   "left join t_price p "
                                                   "on p.f_hardware_id = h.f_id "):
                    result.append({'f_h_id': items.f_h_id,
                                   'f_id': items.f_id,
                                   'f_name': items.f_name,
                                   'f_business_price': items.f_business_price,
                                   'f_cost_price': items.f_cost_price,
                                   'f_description': items.f_description})

            if isinstance(self.request_body['data'], list):
                for items in self.request_body['data']:
                    tmp = None
                    if items.has_key('f_id'):
                        tmp = self.sessions.query(Price).filter(
                            Price.f_id == int(
                                items['f_id'])).one_or_none()

                    if tmp:
                        if isinstance(tmp, list):
                            try:
                                for db_result in tmp:
                                    result.append({'f_id': db_result.f_id,
                                                   'f_name': db_result.f_hardware_id,
                                                   'f_business_price': db_result.f_business_price,
                                                   'f_cost_price': db_result.f_cost_price,
                                                   'f_description': db_result.f_description})
                            except Exception as e:
                                raise AppException(
                                    ret_msg="failed exception: %s" % e.__str__())

                        try:
                            result.append({'f_id': tmp.f_id,
                                           'f_name': tmp.f_hardware_id,
                                           'f_business_price': tmp.f_business_price,
                                           'f_cost_price': tmp.f_cost_price,
                                           'f_description': tmp.f_description})
                        except Exception as e:
                            raise AppException(
                                ret_msg="failed exception: %s" % e.__str__())

            self.jsonify(ret_msg=u"success", data=result)

        if self.request_body['type'] == 'price' and self.request_body[
            'action'] == 'update':
            querys = self.sessions.query(Price)
            if isinstance(self.request_body['data'], list):
                sql = {}
                try:
                    for items in self.request_body['data']:
                        if items.has_key('f_business_price'):
                            sql.update({Price.f_business_price: items['f_business_price']})
                        if items.has_key('f_cost_price'):
                            sql.update({Price.f_cost_price: items['f_cost_price']})
                        if items.has_key('f_description'):
                            sql.update({Price.f_description: items['f_description']})
                        querys.filter(Price.f_id == items['f_id']).update(sql)
                        self.sessions.commit()
                except Exception as e:
                    raise AppException(
                        ret_msg="failed, exception: %s" % e.__str__())

                self.jsonify(ret_msg='success')
