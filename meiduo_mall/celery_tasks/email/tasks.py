# -*- coding: utf-8 -*-
'''
@Time    : 2019-06-26 20:29
@Author  : Leon
@Contact : wangdongjie1994@gmail.com
@File    : tasks.py
@Software: PyCharm
'''
from django.conf import settings
from django.core.mail import send_mail

from celery_tasks.main import celery_app


@celery_app.task(name = 'send_active_email')
def send_active_email(to_email,verify_url):
    """
        发送验证邮箱邮件
        :param to_email: 收件人邮箱
        :param verify_url: 验证链接
        :return: None
    """
    subject = '你好！邮箱验证📮'
    html_message = '<p>尊敬的用户您好！</p>' \
                   '<p>感谢您使用美多商城。</p>' \
                   '<p>您的邮箱为：%s 。请点击此链接激活您的邮箱：</p>' \
                   '<p><a href="%s">%s<a></p>' % (to_email, verify_url, verify_url)

    send_mail(subject, "", settings.EMAIL_FROM, [to_email], html_message=html_message)