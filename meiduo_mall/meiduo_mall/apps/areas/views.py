from django.shortcuts import render

# Create your views here.

# GET /areas/
# class AreasView(ListModelMixin,GenericAPIView):
#     def list(self):
#
#     def get(self):
#         list()
#
#     查询Area数据 复数
#     序列化返回

# GET /areas/<pk>/
# class SubAreasView(RetrieveModelMixin,GenericAPIView):
#     def retrieve(self):
#
#     def get(self):
#         retrieve()
#
#     查询单一的数据对象
#     序列化返回

#   以上是咱们的推导过程，为什么我们最后会选择更加简便的视图集来操作
# class AreasViewSet(ListModelMixin,RetrieveModelMixin,GenericViewSet):
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework_extensions.cache.mixins import CacheResponseMixin

from areas import serializers
from areas.models import Area



class AreasViewSet(CacheResponseMixin,ReadOnlyModelViewSet):
    # queryset = Area.objects.filter(parent = None)
    # serializer_class =  （由于不同的方法对应不同的序列化器，因此重新定义）
    # 没有分页处理的工具
    pagination_class = None
    def get_queryset(self):
        if self.action == 'list':
            return Area.objects.filter(parent = None)
        else:
            return Area.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.AreaSerializer
        else:
            return serializers.SubAreaSerializer



# /areas/ {'get':'list'}  只返回顶级数据 parent = None
# /areas/<pk> {'get':'retrieve'}
# get_object 为什么我通过ID去获取单一值  在查询集里面查询会少值呢？
# get_object 建立在get_queryset 基础之上，以pk 的方式查询 里面的查询集