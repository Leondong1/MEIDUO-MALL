# -*- coding: utf-8 -*-
'''
@Time    : 2019-07-01 21:05
@Author  : Leon
@Contact : wangdongjie1994@gmail.com
@File    : search_indexes.py
@Software: PyCharm
'''
from haystack import indexes

from .models import SKU


class SKUIndex(indexes.SearchIndex, indexes.Indexable):
    """
    SKU索引数据模型类
    """
    #  text 为咱们的组合索引来源
    text = indexes.CharField(document=True, use_template=True)
    id = indexes.IntegerField(model_attr='id')
    name = indexes.CharField(model_attr='name')
    price = indexes.DecimalField(model_attr='price')
    default_image_url = indexes.CharField(model_attr='default_image_url')
    comments = indexes.IntegerField(model_attr='comments')

    def get_model(self):
        """返回建立索引的模型类"""
        return SKU

    def index_queryset(self, using=None):
        """返回要建立索引的数据查询集"""
        return SKU.objects.filter(is_launched=True)