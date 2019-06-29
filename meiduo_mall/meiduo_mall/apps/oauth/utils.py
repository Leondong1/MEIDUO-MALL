# -*- coding: utf-8 -*-
'''
@Time    : 2019-06-23 10:33
@Author  : Leon
@Contact : wangdongjie1994@gmail.com
@File    : utils.py
@Software: PyCharm
'''
from urllib.request import urlopen

from django.conf import settings
# 无论咱们的配置文件怎么写，均可以采用这种方式导入咱们的配置文件
import urllib.parse
import logging
from .exceptions import OAuthQQAPIError
import json
from itsdangerous import TimedJSONWebSignatureSerializer as TJWSSerializer ,BadData
from . import constants

logger = logging.getLogger('django')

class OAuthQQ(object):
    """
    QQ认证辅助工具类
    """
    def __init__(self,client_id = None,client_secret = None,redirect_uri = None,state = None):
        self.client_id = client_id if client_id else settings.QQ_CLIENT_ID
        self.redirect_uri = redirect_uri if redirect_uri else settings.QQ_REDIRECT_URI
        # self.state = state if state else settings.QQ_STATE
        # 另一种写法
        self.state = state or settings.QQ_STATE
        self.client_secret = client_secret if client_secret else settings.QQ_CLIENT_SECRET

    def get_login_url(self):
        url = 'https://graph.qq.com/oauth2.0/authorize?'
        params = {
            'response_type':'code',
            'client_id':self.client_id,
            'redirect_uri':self.redirect_uri,
            'state':self.state
        }

        url += urllib.parse.urlencode(params)
        return url

    def get_access_token(self,code):
        params = {
            'grant_type': 'authorization_code',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': code,
            'redirect_uri': self.redirect_uri,
        }
        url = 'https://graph.qq.com/oauth2.0/token?'
        url += urllib.parse.urlencode(params)

        # 发送请求(存在请求失败或者网络出现异常的情况)
        try:
            resp = urlopen(url)
            # 读取响应体数据
            resp_data = resp.read() # bytes
            resp_data = resp_data.decode() # str

            # 解析 access_token
            resp_dict = urllib.parse.parse_qs(resp_data)
        except Exception as e:
            logger.error('获取access_token异常：%s' % e)
            raise OAuthQQAPIError
        else:
            access_token = resp_dict.get('access_token')

        return access_token[0]

    def get_openid(self,access_token):
        url = 'https://graph.qq.com/oauth2.0/me?access_token=' + access_token
        try:
            # 发送请求
            resp = urlopen(url)
            # 读取响应体数据
            resp_data = resp.read()
            resp_data = resp_data.decode()
            # 返回的数据 callback( {"client_id":"YOUR_APPID","openid":"YOUR_OPENID"} )\n;
            # 解析
            resp_data = resp_data[10:-4]
            resp_dict = json.loads(resp_data)
        except Exception as e:
            logger.error('获取openid异常:%s' % e)
            raise OAuthQQAPIError
        else:
            openid = resp_dict.get('openid', None)
            return openid

    def generate_bind_user_access_token(self,openid):
        serializer = TJWSSerializer(settings.SECRET_KEY,constants.BIND_USER_ACCESS_TOKEN_EXPIRES)
        token = serializer.dumps({'openid':openid})
        return token.decode()

    @staticmethod
    def check_bind_user_access_token(access_token):
        """
        检验保存用户数据的token
        :param token: token
        :return: openid or None
        """
        serializer = TJWSSerializer(settings.SECRET_KEY, constants.BIND_USER_ACCESS_TOKEN_EXPIRES)
        try:
            data = serializer.loads(access_token)
        except BadData:
            return None
        else:
            return data.get('openid')


