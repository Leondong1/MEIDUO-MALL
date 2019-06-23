import random

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from celery_tasks.sms.tasks import send_sms_code
from meiduo_mall.libs.captcha.captcha import captcha
from django_redis import get_redis_connection
from rest_framework import status
import logging

from meiduo_mall.utils.yuntongxun.sms import CCP
from verifications.serializers import ImageCodeCheckSerializer
from . import constants

logger = logging.getLogger('django')


class ImageCodeView(APIView):
    """图片验证码功能实现"""

    # 注意：这里前端传送过来的image_code_id仅作为身份标识，下次在进行传递带上来区分使用
    def get(self, request, image_code_id):
        # 接受参数
        # 检验参数
        # 生成图片验证码
        text, image = captcha.generate_captcha()
        # 保存真实值
        redis_conn = get_redis_connection('verify_codes')
        redis_conn.setex("img_%s" % image_code_id, constants.IMAGE_CODE_REDIS_EXPIRES, text)
        # 返 回图片(了解这里为什么不使用咱们DRF框架里面的Response,因为他会对我们的结果交给render处理，而图片无法解析)
        return HttpResponse(image, content_type='image/jpg')


class SMSCodeView(GenericAPIView):
    serializer_class = ImageCodeCheckSerializer
    """
    短信验证码
    传入参数：
        mobile,   image_code_id, text
    """

    def get(self, request, mobile):
        # 校验参数  （可以交给序列化器实现）
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        sms_code = '%06d' % random.randint(0, 999999)

        # 保存短信验证码 保存发送记录
        redis_conn = get_redis_connection('verify_codes')
        # redis_conn.setex('sms_%s' % mobile,constants.SMS_CODE_REDIS_EXPIRES,sms_code)
        # redis_conn.setex('send_flag_%s' % mobile,constants.SEND_SMS_CODE_INTERVAL,1)

        # redis 管道 (较少咱们的连接次数)
        pl = redis_conn.pipeline()
        pl.setex('sms_%s' % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
        pl.setex('send_flag_%s' % mobile, constants.SEND_SMS_CODE_INTERVAL, 1)

        # 让管道通知redis执行命令
        pl.execute()

        # 发送短信
        # try:
        #     ccp = CCP()
        #     expires = constants.SMS_CODE_REDIS_EXPIRES // 60
        #     result = ccp.send_template_sms(mobile,[sms_code,expires],constants.SMS_CODE_TEMP_ID)
        #
        # except Exception as e:
        #     logger.error("发送验证码短信[异常][ mobile: %s, message: %s ]" % (mobile, e))
        #     return Response({'message':'failed'},status = status.HTTP_500_INTERNAL_SERVER_ERROR)
        # else:
        #     if result == 0:
        #         logger.info("发送验证码短信[正常][ mobile: %s ]" % mobile)
        #         return Response({'message':'ok'})
        #     else:
        #         logger.warning("发送验证码短信[失败][ mobile: %s ]" % mobile)
        #         return Response({'message': 'failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # 使用 celery 发送短信验证码
        expires = constants.SMS_CODE_REDIS_EXPIRES // 60
        send_sms_code.delay(mobile, sms_code, expires, constants.SMS_CODE_TEMP_ID)

        return Response({'message': 'ok'})
