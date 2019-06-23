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
    url(r'^image_codes/(?P<image_code_id>[\w-]+)/$',views.ImageCodeView.as_view()),
    url('^sms_codes/(?P<mobile>1[3-9]\d{9})/$', views.SMSCodeView.as_view()),
]


