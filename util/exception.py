# -*- coding: utf-8 -*-


from tornado.web import HTTPError


class TokenException(Exception):
    pass


class AppException(HTTPError):
    def __init__(self, status_code=500, log_message=None, *args, **kwargs):
        super(AppException, self).__init__(status_code, log_message, *args,
                                           **kwargs)
        self.kwargs = kwargs


class SourcePoolException(Exception):
    pass