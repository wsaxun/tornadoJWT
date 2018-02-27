# -*- coding: utf-8 -*-


import base64
from Crypto.Cipher import AES
from util.parseYaml import conf


class Crypt(object):
    def __init__(self):
        self.key = conf['secretKey']
        self.mode = AES.MODE_CBC

    def encrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.key[0:16])
        length = 16
        count = len(text)
        if (count % length != 0):
            add = length - (count % length)
        # 填充
        text = text + ('\0' * add)
        ciphertext = cryptor.encrypt(text)
        return base64.b64encode(ciphertext)

    def decrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.key[0:16])
        plain_text = cryptor.decrypt(base64.b64decode(text))
        # 解密后，去掉补足的空格用rstrip() 去掉
        return plain_text.rstrip('\0')
