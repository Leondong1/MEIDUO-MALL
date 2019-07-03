# -*- coding: utf-8 -*-
'''
@Time    : 2019-07-02 18:41
@Author  : Leon
@Contact : wangdongjie1994@gmail.com
@File    : serializers.py
@Software: PyCharm
'''
from goods import serializers
from goods.models import SKU


class CartSerializer(serializers.Serializer):
    """
    购物车数据序列化器
    """
    sku_id = serializers.IntegerField(label='sku id ', min_value=1)
    count = serializers.IntegerField(label='数量', min_value=1)
    selected = serializers.BooleanField(label='是否勾选', default=True)

    def validate(self, data):
        try:
            sku = SKU.objects.get(id=data['sku_id'])
        except SKU.DoesNotExist:
            raise serializers.ValidationError('商品不存在')

        if data['count'] > sku.stock:
            raise serializers.ValidationError('商品库存不足')

        return data