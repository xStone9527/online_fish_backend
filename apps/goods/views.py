from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import GoodsSerializer,GoodsCategorySerializer,BannerSerializer,IndexGoodsSerializer
from rest_framework import status
from .models import Goods,GoodsCategory,Banner
from rest_framework import mixins
from rest_framework import generics
from  rest_framework.pagination import PageNumberPagination
from  rest_framework.viewsets  import GenericViewSet
from django_filters.rest_framework import DjangoFilterBackend
from .filters import GoodsFilter
from rest_framework.filters import SearchFilter
from rest_framework.filters import OrderingFilter
from rest_framework.authentication import TokenAuthentication
from rest_framework_extensions.cache.mixins import CacheResponseMixin


class DefaultResultsSetPagination(PageNumberPagination):
    page_size = 12  #默认单页面10个
    page_size_query_param = 'page_size' #可通过该参数自己设置每页多少个
    page_query_param = "page"  #t通过该参数选择多少页
    max_page_size = 100     #通过url修改参数  最大单页面100个


class GoodsListViewSet(CacheResponseMixin,mixins.ListModelMixin,mixins.RetrieveModelMixin,GenericViewSet):
    """
    商品列表 分页 过滤 搜索 排序
    """

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.click_num +=1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    queryset = Goods.objects.get_queryset().order_by('id')
    serializer_class = GoodsSerializer
    pagination_class = DefaultResultsSetPagination
    filter_backends = (DjangoFilterBackend,SearchFilter,OrderingFilter)
    # authentication_classes = (TokenAuthentication,)
    filter_class = GoodsFilter
    search_fields = ('name', 'goods_brief','goods_desc')
    ordering_fields = ('shop_price','sold_num')



class GoodsCategoryViewSet(mixins.ListModelMixin,mixins.RetrieveModelMixin,GenericViewSet):
    """
    list:
        商品分类列表数据
    retrieve:
        商品类型详情。
    """

    queryset =  GoodsCategory.objects.filter(category_type=1)
    serializer_class = GoodsCategorySerializer
    # filter_backends = (DjangoFilterBackend,)
    # filter_fields = ('name', 'category_type') #过滤字段

    # def get_queryset(self):
    #     all_goodsCategory = GoodsCategory.objects.all()
    #     return all_goodsCategory.filter(category_type=1)



class BannerViewset(mixins.ListModelMixin,GenericViewSet):
    """
    list:
        获取轮播图列表
    """
    queryset = Banner.objects.all().order_by("index")
    serializer_class = BannerSerializer

class IndexCategoryViewSet(mixins.ListModelMixin,GenericViewSet):
    """
    首页商品分类数据
    """
    queryset = GoodsCategory.objects.filter(is_tab=True,name__in=["生鲜食品","酒水饮料"])
    serializer_class = IndexGoodsSerializer


