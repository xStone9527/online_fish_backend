# -*- coding: utf-8 -*-

__author__ = 'xl'
"""
__date__ = TIME： 2018/08/18 上午9:52
describe:
"""
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from goods.serializers import GoodsSerializer

from .models import UserFav,UserLeavingMessage,UserAddress

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

class UserLeavingMessageSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()   #用户设置默认值 当前用户
    )
    add_time = serializers.DateTimeField(read_only=True,format='%Y-%m-%d %H:%M')#只读不写，设置相应显示格式
    class Meta:
        model = UserLeavingMessage
        fields = ("id","user","message_type","subject","message","file","add_time")

class UserAddressSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()   #用户设置默认值 当前用户
    )
    class Meta:
        model = UserAddress
        fields = ("id","user","province","city","district","address","signer_name","signer_mobile")


