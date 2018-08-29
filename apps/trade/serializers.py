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
from utils.alipay import AliPay
from fish_site.settings import ali_pub_key_path,private_key_path

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
    alipay_url = serializers.SerializerMethodField(read_only=True)

    def get_alipay_url(self,obj):
        alipay = AliPay(
            appid="2016091700534234",
            app_notify_url="http://101.132.194.31:8000/alipay/return/",
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,  沙箱环境用True
            return_url="http://101.132.194.31:8000/alipay/return/"
        )

        url = alipay.direct_pay(
            subject=obj.order_sn,
            out_trade_no=obj.order_sn,
            total_amount=obj.order_mount,
        )
        re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)
        return re_url

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
    alipay_url = serializers.SerializerMethodField(read_only=True)

    def get_alipay_url(self,obj):
        alipay = AliPay(
            appid="2016091700534234",
            app_notify_url="http://101.132.194.31:8000/alipay/return/",
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,  沙箱环境用True
            return_url="http://101.132.194.31:8000/alipay/return/"
        )

        url = alipay.direct_pay(
            subject=obj.order_sn,
            out_trade_no=obj.order_sn,
            total_amount=obj.order_mount,
        )
        re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)
        return re_url


    class Meta:
        model =OrderInfo
        fields ="__all__"


