# -*- coding: utf-8 -*-
'''
@Time    : 2019-07-01 19:02
@Author  : Leon
@Contact : wangdongjie1994@gmail.com
@File    : serializers.py
@Software: PyCharm
'''
from rest_framework import serializers
from goods.search_indexes import SKUIndex
from .models import SKU
from drf_haystack.serializers import HaystackSerializer


class SKUSerializer(serializers.ModelSerializer):
    class Meta:
        model = SKU
        fields = ('id','name','price','default_image_url','comments')


class SKUIndexSerializer(HaystackSerializer):
    """
    SKU索引结果数据序列化器
    """
    class Meta:
        index_classes = [SKUIndex]
        fields = ('text', 'id', 'name', 'price', 'default_image_url', 'comments')