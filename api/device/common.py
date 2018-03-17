# -*- coding: utf-8 -*-


class CheckParams(object):
    """
    参数检测
    """

    PARAMS = ['action', 'type', 'data']

    def _check_params(self):
        body = self.request_body.keys()
        return set(self.PARAMS).issubset(set(body))