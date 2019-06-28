# -*- coding: utf-8 -*-
'''
@Time    : 2019-06-20 16:40
@Author  : Leon
@Contact : wangdongjie1994@gmail.com
@File    : main.py
@Software: PyCharm
'''
from celery import Celery


# 为celery使用django配置文件进行设置（因为咱们的任务执行涉及到 django里面的配置）
import os
if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'meiduo_mall.settings.dev'

# 创建celery应用
celery_app = Celery('meiduo')

# 导入celery配置
celery_app.config_from_object('celery_tasks.config')

# 导入任务（因为在启动咱们的任务的时候，还不能自动识别，需要指明）
celery_app.autodiscover_tasks(['celery_tasks.sms','celery_tasks.email'])


