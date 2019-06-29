# -*- coding: utf-8 -*-
'''
@Time    : 2019-06-29 10:02
@Author  : Leon
@Contact : wangdongjie1994@gmail.com
@File    : serializers.py
@Software: PyCharm
'''
from rest_framework import serializers

from areas.models import Area


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ('id','name')


class SubAreaSerializer(serializers.ModelSerializer):
    # 牢记咱们的 外键里面序列化器使用需指明的参数： read_only
    # 或者queryset
    subs = AreaSerializer(many=True, read_only=True)
    class Meta:
        model = Area
        # subs 外键使用关联对象的序列化器，并且该对象是一个
        # 包含多个字典的列表，因此 many = True
        fields = ('id','name','subs')