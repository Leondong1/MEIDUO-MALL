from django.shortcuts import render

# Create your views here.

# url(r'^usernames/(?P<username>\w{5,20})/count/$', views.UsernameCountView.as_view()),
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users import serializers
from users.models import User

# url(r'^users/$', views.UserView.as_view())
from users.serializers import UserDetailSerializer


class UserView(CreateAPIView):
    """
    用户注册
    传入参数
    """
    serializer_class = serializers.CreateUserSerializer

class UsernameCountView(APIView):
    """
    用户名数量
    """
    def get(self, request, username):
        """
        获取指定用户名数量
        """
        count = User.objects.filter(username=username).count()

        data = {
            'username': username,
            'count': count
        }

        return Response(data)

# url(r'^mobiles/(?P<mobile>1[3-9]\d{9})/count/$', views.MobileCountView.as_view()),
class MobileCountView(APIView):
    """
    手机号数量
    """
    def get(self, request, mobile):
        """
        获取指定手机号数量
        """
        count = User.objects.filter(mobile=mobile).count()

        data = {
            'mobile': mobile,
            'count': count
        }

        return Response(data)

# GET /user/
class UserDetailView(RetrieveAPIView):
    """用户基本信息"""
    serializer_class = serializers.UserDetailSerializer
    # 因为咱们这里没有去指明具体的哪一个用户，因此，需要知道已经是登录过的用户(权限验证)
    permission_classes = [IsAuthenticated]
    # queryset = User.objects.all()
    def get_object(self):
        # self.get_queryset.get(pk = pk)  =  self.get_object()
        # 返回当前请求的用户
        # 在类视图当中，可以通过类视图对象的属性获取request
        # 在Django的请求request对象中，user属性表明当前请求的用户
        return self.request.user

# PUT /email/
class EmailView(UpdateAPIView):
    serializer_class = serializers.EmailSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

# url(r'^emails/verification/$', views.VerifyEmailView.as_view()),
class VerifyEmailView(APIView):
    """
    邮箱验证
    """
    def get(self, request):
        # 获取token
        token = request.query_params.get('token')
        if not token:
            return Response({'message': '缺少token'}, status=status.HTTP_400_BAD_REQUEST)

        # 验证token
        user = User.check_verify_email_token(token)
        if user is None:
            return Response({'message': '链接信息无效'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            user.email_active = True
            user.save()
            return Response({'message': 'OK'})

