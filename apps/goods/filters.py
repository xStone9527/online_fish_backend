# -*- coding: utf-8 -*-

__author__ = 'xl'
"""
__date__ = TIME： 2018/07/08 下午11:08
describe:
"""
from django_filters import rest_framework as filters
from .models import Goods
from django.db.models import Q

class GoodsFilter(filters.FilterSet):
    """
    商品的过滤类
    """
    pricemin = filters.NumberFilter(name="shop_price", lookup_expr='gte',help_text ="最小价格")
    pricemax = filters.NumberFilter(name="shop_price", lookup_expr='lte')
    name = filters.CharFilter(name ="name",lookup_expr='contains')
    top_category = filters.NumberFilter(method='top_category_filter')
    def top_category_filter(self,queryset,name,value):
         return queryset.filter(Q(category_id =value)\
                                |Q(category__parent_category =value)\
                                |Q( category__parent_category__parent_category = value))


    class Meta:
        model = Goods
        fields = ['name', 'pricemin', 'pricemax','is_hot',]


