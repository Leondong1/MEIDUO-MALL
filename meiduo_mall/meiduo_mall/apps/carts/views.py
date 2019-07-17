import base64
import pickle

from django.shortcuts import render

# Create your views here.
from django_redis import get_redis_connection
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from carts.serializers import CartSerializer,CartSKUSerializer
from goods.models import SKU
from . import constants


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

        #  判断用户登录状态
        try:
            user = request.user
        except Exception:
            user = None

        # 保存
        if user and user.is_authenticated:
            # 如果用户已登录，保存到redis
            redis_conn = get_redis_connection('cart')
            pl = redis_conn.pipeline()
            # 用户购物车数据 redis hash
            pl.hincrby('cart_%s' % user.id,sku_id,count)
            # 用户购物车勾选数据  redis set
            if selected:
                pl.sadd('cart_selected_%s' % user.id,sku_id)

            pl.execute()
            return Response(serializer.data)
        else:
            # 如果用户未登录，保存到cookie
            # 取出cookie 中的购物车数据
            cart_str = request.COOKIES.get('cart')
            if cart_str:
                # 解析
                cart_str = cart_str.encode()
                # 将bytes类型进行base64 解码 咱们的base64无论编码还是解码均是对于bytes类型
                cart_bytes = base64.b64decode(cart_str)
                cart_dict = pickle.loads(cart_bytes)
            else:
                cart_dict = {}
            # 如果商品存在购物车中，累加
            if sku_id in cart_dict:
                cart_dict[sku_id]['count'] += count
                cart_dict[sku_id]['selected'] = selected
            # 如果商品不再购物车中，设置
            else:
                cart_dict[sku_id] = {
                    'count':count,
                    'selected':selected
                }

            cart_cookie = base64.b64encode(pickle.dumps(cart_dict)).decode()
            # 设置cookie
            response = Response(serializer.data)
            response.set_cookie('cart',cart_cookie,max_age=constants.CART_COOKIE_EXPIRES)

            return response

    def get(self,request):
        """查询购物车"""
        # 判断用户登录状态
        try:
            user = request.user
        except Exception:
            user = None

        # 保存
        if user and user.is_authenticated:
            # 如果用户已经登录，从redis中查询 sku_id count selected
            redis_conn = get_redis_connection('cart')
            redis_cart = redis_conn.hgetall('cart_%s' % user.id)

            #redis_cart = {
                # 商品的sku_id  bytes字节类型:数量  bytes字节类型
                # 也就是说从咱们的数据库取出来的时候 变为了 bytes 类型
            #}
            redis_cart_selected = redis_conn.smembers('cart_selected_%s' % user.id)

            # 遍历redis_cart,形成cart_dict
            cart_dict = {}
            for sku_id, count in redis_cart.items():
                cart_dict[int(sku_id)] = {
                    'count':int(count),
                    'selected': sku_id in redis_cart_selected
                }
        else:
            # 如果用户未登录，从cookie中查询
            cookie_cart = request.COOKIES.get('cart')

            if cookie_cart:
                # 表示cookie中有购物车数据
                cart_dict = pickle.loads(base64.b64encode(cookie_cart.encode()))
            else:
                cart_dict = {}

        # 查询数据库
        sku_id_list = cart_dict.keys()
        sku_obj_list = SKU.objects.filter(id__in = sku_id_list)

        # 遍历sku_obj_list 向sku对象中添加count 和 selected 属性
        for sku in sku_obj_list:
            sku.count = cart_dict[sku.id]['count']
            sku.selected = cart_dict[sku.id]['selected']

        # 序列化返回
        serializer = CartSKUSerializer(sku_obj_list,many = True)
        return Response(serializer.data)

    def put(self,request):
        """修改购物车"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 从序列化器里面取出验证保存的数据方式
        sku_id = serializer.validated_data['sku_id']
        count = serializer.validated_data['count']
        selected = serializer.validated_data['selected']

        # 判断用户的登录状态
        try:
            user = request.user
        except Exception:
            user = None

        # 保存
        if user and user.is_authenticated:
            # 如果用户已经登录，修改redis
            redis_conn = get_redis_connection('cart')
            pl = redis_conn.pipeline()

            # 处理数量 hash
            pl.hset('cart_%s' % user.id,sku_id,count)

            # 处理勾选状态
            if selected:
                # 表示勾选
                pl.sadd('cart_selected_%s' % user.id,sku_id)
            else:
                # 表示取消勾选，删除
                pl.srem('cart_selected_%s' % user.id,sku_id)
            pl.execute()
            return Response(serializer.data)

        else:
            # 未登录，修改cookie
            cookie_cart = request.COOKIES.get('cart')

            if cookie_cart:
                # 表示cookie中有购物车数据
                # 解析
                cart_dict = pickle.loasds(base64.b64decode(cookie_cart.encode()))
            else:
                # 表示cookie中没有购物车数据
                cart_dict = {}

            response = Response(serializer.data)
            if sku_id in cart_dict:
                cart_dict[sku_id] = {
                    'count':count,
                    'selected':selected
                }

                cart_cookie = base64.b64encode(pickle.dumps(cart_dict)).decode()
                # 设置cookie
                response.set_cookie('cart', cart_cookie, max_age=constants.CART_COOKIE_EXPIRES)

            return response