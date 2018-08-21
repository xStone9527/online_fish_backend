# -*- coding: utf-8 -*-

__author__ = 'xl'
"""
__date__ = TIME： 2018/08/19 上午10:31
describe:
"""
import time
import random
from string import digits

from rest_framework import serializers

from .models import ShoppingCart,OrderInfo,OrderGoods
from goods.models import Goods
from goods.serializers import GoodsSimpleSerializer

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
    def update(self, instance, validated_data):
        #修改商品数量
        instance.nums = validated_data['nums']
        instance.save()
        return instance

class UserCartDetailSerializer(serializers.ModelSerializer):
    goods = GoodsSimpleSerializer(many=False)
    class Meta:
        model = ShoppingCart
        fields =('id','nums','goods')

class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()   #用户设置默认值 当前用户
    )
    pay_status =serializers.CharField(read_only=True)
    order_sn = serializers.CharField(read_only=True)
    trade_no = serializers.CharField(read_only=True)
    pay_time = serializers.DateTimeField(read_only=True)
    def generate_soder_sn(self):
        """
        当前时间 + userid + 随机数
        """
        order_sn ="{time_str}{useid}{ranstr}".format(\
            time_str= time.strftime("%Y%m%d%H%M%S"),\
            useid=self.context['request'].user.id,\
            ranstr =''.join(random.sample(digits, 6)))
        return  order_sn

    def validate(self, attrs):
        attrs['order_sn'] = self.generate_soder_sn()
        return attrs

    class Meta:
        model = OrderInfo
        fields = "__all__"


class OrderGoodsSerializer(serializers.ModelSerializer):
    goods = GoodsSimpleSerializer(many=False)
    class Meta:
        model =OrderGoods
        fields ="__all__"

class OrderDetailSerializer(serializers.ModelSerializer):
    goods = OrderGoodsSerializer(many=True)
    class Meta:
        model =OrderInfo
        fields ="__all__"