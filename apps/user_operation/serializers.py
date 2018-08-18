# -*- coding: utf-8 -*-

__author__ = 'xl'
"""
__date__ = TIME： 2018/08/18 上午9:52
describe:
"""
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from goods.serializers import GoodsSerializer

from .models import UserFav

class UserFavSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()   #用户设置默认值 当前用户
    )
    """
    用户收藏序列化
    """

    class Meta:
        model = UserFav
        fields =  ('user',"goods", "id")  #删除时需要返回id信息 故此时ID也添加
        validators = [                  #唯一型设置方式2 方式1是在models中添加联合唯一型索引
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields=('user', 'goods'),
                message = "已经收藏,不需要再创建  "
            )
        ]

class UserFavDetailSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer()

    class Meta:
        model = UserFav
        fields = ("goods", "id")
