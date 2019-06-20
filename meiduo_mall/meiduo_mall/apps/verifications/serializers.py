# -*- coding: utf-8 -*-
'''
@Time    : 2019-06-18 20:21
@Author  : Leon
@Contact : wangdongjie1994@gmail.com
@File    : serializers.py
@Software: PyCharm
'''
from django_redis import get_redis_connection
from rest_framework import serializers

class ImageCodeCheckSerializer(serializers.Serializer):
    """
    图片验证码校验序列化器
    注意：定义的时候指明咱们的参数字段类型以及检验的方式
    """
    image_code_id = serializers.UUIDField()
    text = serializers.CharField(max_length=4,min_length=4)

    def validate(self, attrs):
        image_code_id = attrs['image_code_id']
        text = attrs['text']

        # 查询真实图片验证码
        redis_conn = get_redis_connection('verify_codes')
        real_image_code_text = redis_conn.get('img_%s' % image_code_id)
        # 无效的原因：不存在该 image_code_id 或者 图片验证码过期
        if not real_image_code_text:
            raise serializers.ValidationError('图片验证码无效')

        # 删除Redis中的图片验证码(为了防止使用一个验证码多次匹配)
        redis_conn.delete('img_%s' % image_code_id)


        # 比较图片验证码
        real_image_code_text = real_image_code_text.decode()
        if real_image_code_text.lower() != text.lower():
            raise serializers.ValidationError('图片验证码错误')

        # 判断是否在60s内
        # get_serializer 方法在创建序列化器对象的时候，会补充 context 属性
        # context 属性中包含三个值 request  format  view 类视图对象
        # self.context('view')

        # django 的类视图对象中，kwargs 属性保存了路径提取出来的参数
        mobile = self.context['view'].kwargs['mobile']
        # 思路：关于这条记录如果存在，一定是在咱们的Redis有效期内 不存在（不再有效期或者没有该记录）
        send_flag = redis_conn.get('send_flag_%s' % mobile)
        if send_flag:
            raise serializers.ValidationError('请求次数过于频繁')

        return attrs


