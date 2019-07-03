from django.shortcuts import render

# Create your views here.
from rest_framework.generics import GenericAPIView

from carts.serializers import CartSerializer


class CartView(GenericAPIView):
    """购物车模块"""
    # 获取数据并进行校验
    serializer_class = CartSerializer

    def perform_authentication(self, request):
        """将执行具体请求前的身份认证关掉，由视图函数自己执行身份认证"""
        pass

    def post(self,request):
        # sku_id count selected
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)

        # 从序列化器里面取出验证保存的数据方式
        sku_id = serializer.validated_data['sku_id']
        count = serializer.validated_data['count']
        selected = serializer.validated_data['selected']

