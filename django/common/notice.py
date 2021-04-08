import requests
import json
import sys
import time
import hmac
import hashlib
import base64
import urllib.parse
from django.conf import settings


class notice:

    def __init__(self, **kwargs):
        pass

    def send(self):
        pass

    # 限速、重复发送
    def rate(self):
        pass


class email(notice):

    def send(self):
        pass


class wechat(notice):

    def send(self):
        pass


class sms(notice):

    def send(self):
        pass


class dingding(notice):
    secret = settings.DING_SIGN_SECRET
    access_token = settings.DING_ACCESS_TOKEN

    # 发送消息
    @classmethod
    def send(cls, title, content, users=[], at_all=False):

        url = 'https://oapi.dingtalk.com/robot/send?access_token={}&timestamp={}&sign={}'
        sign, timestamp = cls._gen_signature()

        headers = {
            'Content-Type': 'application/json'
        }

        data = {
            "msgtype": "markdown",
            "markdown": {
                "title": title,
                "text": content
            },
            "at": {
                # 使用 markdown 类型，被at人的手机号需要在text内容中存在
                "atMobiles": users,
                "isAtAll": at_all
            }
        }
        resp = requests.post(url=url.format(cls.access_token, timestamp,
                                            sign), json=data, headers=headers)

    # 生成签名
    @classmethod
    def _gen_signature(cls):
        '''
        签名密钥
        return：签名，时间戳
        '''
        secret_enc = cls.secret.encode('utf-8')
        timestamp = str(round(time.time() * 1000))
        string_to_sign = '{}\n{}'.format(timestamp, cls.secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc,
                             digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        return sign, timestamp
