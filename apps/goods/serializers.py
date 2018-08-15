# -*- coding: utf-8 -*-

__author__ = 'xl'
"""
__date__ = TIME： 2018/07/08 上午11:15
describe:
"""
from rest_framework import serializers

from .models import Goods,GoodsCategory

class GoodsCategorySerializer3(serializers.ModelSerializer):
    """
    商品类别序列化
    """

    class Meta:
        model = GoodsCategory
        fields = "__all__"
class GoodsCategorySerializer2(serializers.ModelSerializer):
    """
    商品类别序列化
    """
    sub_cat =GoodsCategorySerializer3(many=True)
    class Meta:
        model = GoodsCategory
        fields = "__all__"

class GoodsCategorySerializer(serializers.ModelSerializer):
    """
    商品类别序列化
    """
    sub_cat =GoodsCategorySerializer2(many=True)
    class Meta:
        model = GoodsCategory
        fields = "__all__"


class GoodsSerializer(serializers.ModelSerializer):
    category = GoodsCategorySerializer()
    class Meta:
        model = Goods
        fields ="__all__"


