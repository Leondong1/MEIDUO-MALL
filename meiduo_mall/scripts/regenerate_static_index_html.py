# -*- coding: utf-8 -*-
'''
@Time    : 2019-06-30 07:05
@Author  : Leon
@Contact : wangdongjie1994@gmail.com
@File    : regenerate_static_index_html.py
@Software: PyCharm
'''
#!/usr/bin/env python

import sys
sys.path.insert(0, '../')

import os
if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'meiduo_mall.settings.dev'

# 将Django的配置文件及运行环境运行起来
import django
django.setup()


from contents.crons import generate_static_index_html


if __name__ == '__main__':
    generate_static_index_html()
