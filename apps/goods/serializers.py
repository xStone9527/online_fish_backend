# -*- coding: utf-8 -*-

__author__ = 'xl'
"""
__date__ = TIME： 2018/07/08 上午11:15
describe:
"""
from rest_framework import serializers

from .models import Goods,GoodsCategory,GoodsImage

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

class GoodsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsImage
        fields = ('image',)

class GoodsSerializer(serializers.ModelSerializer):
    category = GoodsCategorySerializer()
    images = GoodsImageSerializer(many=True)   # 因为GoodsImage 关联Good 的 relax_name 为 images
    class Meta:
        model = Goods
        fields ="__all__"


class GoodsSimpleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Goods
        fields ="__all__"


