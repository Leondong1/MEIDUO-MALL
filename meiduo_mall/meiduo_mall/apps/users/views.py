from django.shortcuts import render

# Create your views here.

# url(r'^usernames/(?P<username>\w{5,20})/count/$', views.UsernameCountView.as_view()),
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from users import serializers, constants
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

class AddressViewSet(CreateModelMixin,UpdateModelMixin,GenericViewSet):
    """
    用户地址新增与修改
    """
    serializer_class = serializers.UserAddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.addresses.filter(is_deleted = False)

    # GET /addresses/
    def list(self,request,*args,**kwargs):
        """
        用户地址列表数据
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        querset = self.get_queryset()
        serializer = self.get_serializer(querset,many = True)
        user = self.request.user
        return Response({
            'user_id': user.id,
            'default_address_id': user.default_address_id,
            'limit': constants.USER_ADDRESS_COUNTS_LIMIT,
            'addresses': serializer.data,
        })

    # POST /addresses/
    def create(self, request, *args, **kwargs):
        # 检查用户地址数据数目不能超过上限
        count = request.user.addresses.count()
        if count >= constants.USER_ADDRESS_COUNTS_LIMIT:
            return Response({'message':'保存用户地址达到上限'},status=status.HTTP_400_BAD_REQUEST)

        return super().create(request,*args,**kwargs)

    # delete /addresses/<pk>
    def destory(self,request,*args,**kwargs):
        address = self.get_object()

        # 进行逻辑删除
        address.is_deleted = True
        address.save()

        return Response(status = status.HTTP_204_NO_CONTENT)

    # put /addresses/pk/status
    @action(methods= ['put'],detail = True)
    def status(self,request,pk = None):
        """
        设置默认地址
        :param request:
        :param pk:
        :return:
        """
        address = self.get_object()
        request.user.default_address = address
        request.user.save()
        return  Response({'message':'ok'},status = status.HTTP_200_OK)

    # put /addresses/pk/title/
    # 需要请求体参数 title
    @action(methods=['put'], detail=True)
    def title(self, request, pk=None):
        """
        修改标题
        """
        address = self.get_object()
        serializer = serializers.AddressTitleSerializer(instance=address, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)