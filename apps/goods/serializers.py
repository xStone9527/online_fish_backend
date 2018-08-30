# -*- coding: utf-8 -*-

__author__ = 'xl'
"""
__date__ = TIME： 2018/07/08 上午11:15
describe:
"""
from rest_framework import serializers
from django.db.models import Q

from .models import Goods,GoodsCategory,GoodsImage,Banner,GoodsCategoryBrand,IndexAd

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

class BannerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Banner
        fields ="__all__"
class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = GoodsCategoryBrand
        fields ="__all__"

class IndexGoodsSerializer(serializers.ModelSerializer):
    brands = BrandSerializer(many=True)
    goods = serializers.SerializerMethodField()
    sub_cat = GoodsCategorySerializer2(many=True)
    ad_goods = serializers.SerializerMethodField()
    def get_ad_goods(self,obj):
        goods = {}
        ad_goods = IndexAd.objects.filter(category_id=obj.id)  # 单下划线过滤
        if ad_goods:
            good_ins = ad_goods[0].goods
            goods_json = GoodsSerializer(good_ins,many=False,context={'request':self.context['request']}).data
        return goods_json


    def get_goods(self,obj):
        all_goods = Goods.objects.filter(Q(category_id =obj.id)\
                                |Q(category__parent_category =obj.id)\
                                |Q( category__parent_category__parent_category = obj.id))

        goods_serializer = GoodsSerializer(all_goods,many=True,context={'request':self.context['request']})
        return goods_serializer.data



    class Meta:
        model = GoodsCategory
        fields ="__all__"


