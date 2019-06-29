from django.shortcuts import render

# Create your views here.

#  url(r'^qq/authorization/$', views.QQAuthURLView.as_view()),
from rest_framework import request, status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings

from oauth.exceptions import OAuthQQAPIError
from oauth.utils import OAuthQQ
from .models import OAuthQQUser
from .serializers import OAuthQQUserSerializer



#  url(r'^qq/authorization/$', views.QQAuthURLView.as_view()),
class QQAuthURLView(APIView):
    """
    获取QQ登录的URL地址
    1. 获取next参数
    2. 拼接QQ登录的网址
    3. 返回
    """
    def get(self,request):
        next = request.query_params.get('next')
        oauth_qq = OAuthQQ(state = next)
        login_url = oauth_qq.get_login_url()

        return Response({'login_url':login_url})

class QQAuthUserView(CreateAPIView):
    """
    qq登录的用户
    """
    serializer_class = OAuthQQUserSerializer

    def get(self,request):
        # 获取qq登录的用户数据
        code = request.query_params.get('code')
        if not code:
            return Response({'message': '缺少code'}, status=status.HTTP_400_BAD_REQUEST)

        oauth_qq = OAuthQQ()

        # 获取用户openid
        try:
            access_token = oauth_qq.get_access_token(code)
            openid = oauth_qq.get_openid(access_token)
        except OAuthQQAPIError:
            return Response({'message': 'QQ服务异常'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        # 根据openid查询数据库OAuthQQUser  判断数据是否存在
        try:
            oauth_qq_user = OAuthQQUser.objects.get(openid = openid)
        except OAuthQQUser.DoesNotExist:
            # 如果数据不存在，处理openid并返回
            access_token = oauth_qq.generate_bind_user_access_token(openid)
            return Response({'access_token':access_token})

        else:
            # 如果数据存在，表示用户已经绑定过身份，签发JWT_TOKEN
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

            user = oauth_qq_user.user
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)

            return Response({
                'username':user.username,
                'user_id':user.id,
                'token':token
            })

    # """
    # def post(self, request, *args, **kwargs):
    # :param request:
    # :param args:
    # :param kwargs:
    # :return:
    # 获取数据
    # 校验数据
    # 判断用户是否存在
    # 如果存在，绑定，创建OAuthQQUser数据
    #
    # 如果不存在，先创建User,创建OAuthQQUser数据
    #
    # 签发JWT token
    # """

