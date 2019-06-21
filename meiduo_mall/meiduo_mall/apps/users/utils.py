# -*- coding: utf-8 -*-
'''
@Time    : 2019-06-21 08:10
@Author  : Leon
@Contact : wangdongjie1994@gmail.com
@File    : utils.py
@Software: PyCharm
'''
from django.contrib.auth.backends import ModelBackend


def jwt_response_payload_handler(token, user=None, request=None):
    """
    自定义jwt认证成功返回数据
    改写咱们的返回值
    """
    return {
        'token': token,
        'user_id': user.id,
        'username': user.username
    }

class UsernameMobileAuthBackend(ModelBackend):
    """
    自定义用户名或手机号认证
    """
