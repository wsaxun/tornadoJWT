# -*- coding: utf-8 -*-

from tornado.web import RequestHandler
from tornado.gen import coroutine
from api.handle.mixin import (RestfulMixin, CreateSessionMixin, OperationMixin)
from data.models import ConfigHistory, Product
from sqlalchemy import desc, asc
from util.exception import AppException


class Historys(OperationMixin, CreateSessionMixin, RestfulMixin,
               RequestHandler):
    """
    历史数据展示
    前端传递数据：
        {action: query, type: history, pageSize: 1, pageNumber:2}
    """

    @coroutine
    def post(self):
        if self.request_body['type'] == 'history' and self.request_body[
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

        if self.request_body['type'] == 'history' and self.request_body[
            'action'] == 'query':
            result = []
            if self.request_body.has_key('sort'):
                sort = self.request_body['sort']
                if sort == 'f_id':
                    sorts = ConfigHistory.f_id
                elif sort == 'f_create_time':
                    sorts = ConfigHistory.f_create_time
                elif sort == 'f_name':
                    sorts = Product.f_name
                else:
                    sorts = ConfigHistory.f_id

                if self.request_body.has_key('order'):
                    order = self.request_body['order']
                    if order == 'desc':
                        sorts = desc(sorts)
                    else:
                        sorts = asc(sorts)

            if self.request_body.has_key('search'):
                search = self.request_body['search']


                total_record = self.sessions.query(ConfigHistory,
                                                   Product.f_name).join(
                    Product).filter(Product.f_name.like('%'+'%s' %(search) +'%')).order_by(sorts)
            else:
                total_record = self.sessions.query(ConfigHistory,
                                                   Product.f_name).join(
                    Product).order_by(sorts)

            total = total_record.count()
            for items in total_record.limit(
                    self.request_body['limit']).offset(
                self.request_body['offset']):
                result.append({'f_id': items[0].f_id,
                               'f_create_time': items[
                                   0].f_create_time.__str__(),
                               'f_name': items[1],
                               'f_config': items[0].f_config,
                               'f_description': items[0].f_description})
            self.jsonify(ret_msg=u"success", total=total, data=result)
        else:
            raise AppException(ret_msg=u'args error')

        if self.request_body['type'] == 'product':
            raise AppException(ret_msg=u'unsupported action')

        raise AppException(ret_msg=u'type error')
