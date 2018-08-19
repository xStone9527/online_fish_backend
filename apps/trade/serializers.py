# -*- coding: utf-8 -*-

__author__ = 'xl'
"""
__date__ = TIME： 2018/08/19 上午10:31
describe:
"""
from rest_framework import serializers

from .models import ShoppingCart
from goods.models import Goods

class UserShopingCartSerializer(serializers.Serializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()   #用户设置默认值 当前用户
    )
    goods = serializers.PrimaryKeyRelatedField(required=True,queryset=Goods.objects.all())
    nums = serializers.IntegerField(required=True,min_value=1,help_text="商品数量",
                                   error_messages = {
                                       "min_value":"商品数量不能小于1",
                                       "required":"请填写购买数量"
                                   })
    def create(self, validated_data):
        user = self.context["request"].user
        nums = validated_data['nums']
        goods = validated_data['goods']

        existd = ShoppingCart.objects.filter(user=user,goods=goods)
        if existd:
            existd = existd[0]
            existd.nums += nums
            existd.save()
        else:
            existd = ShoppingCart.objects.create(**validated_data)
        return existd