# -*- coding: utf-8 -*-

import time
import json
import jwt
from util.exception import TokenException
from util.parseYaml import conf


class Token(object):
    def __init__(self):
        self.token_exp = conf['tokenExp']
        self.secret_key = conf['secretKey']
        self.algorithm = 'HS256'
        self.iat = int(time.time())
        self.exp = int(self.iat + self.token_exp * 60 * 60)

    def _crete_playload(self, **kwargs):
        default_playload = {'iat': self.iat, 'exp': self.exp}
        playload = {}
        if kwargs:
            playload = json.loads(json.dumps(dict(default_playload, **kwargs)))
        return playload or default_playload

    def entoken(self, **kwargs):
        playload = self._crete_playload(**kwargs)
        try:
            token = jwt.encode(playload, self.secret_key, algorithm=self.algorithm)
        except Exception as e:
            raise TokenException(e.message)
        return token

    def detoken(self, token):
        try:
            data = jwt.decode(token, self.secret_key, algorithms=self.algorithm)
        except jwt.ExpiredSignatureError:
            raise TokenException("Signature has expired")
        except jwt.DecodeError:
            raise TokenException("decode token error")
        except Exception as e:
            raise TokenException(e.message)
        return data

