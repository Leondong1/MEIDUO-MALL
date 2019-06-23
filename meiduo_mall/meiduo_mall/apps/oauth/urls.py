# -*- coding: utf-8 -*-
'''
@Time    : 2019-06-18 02:47
@Author  : Leon
@Contact : wangdongjie1994@gmail.com
@File    : urls.py
@Software: PyCharm
'''
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^qq/authorization/$',views.QQAuthURLView.as_view()),
    url(r'^qq/user/$',views.QQAuthUserView.as_view()),
]


