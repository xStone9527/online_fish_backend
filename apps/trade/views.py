from django.shortcuts import render

# Create your views here.
import time
import string
import random
from datetime import datetime
from django.shortcuts import redirect
from rest_framework import viewsets,permissions,authentication,mixins
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from user_operation.permissions import IsOwnerOrReadOnly
from .models import ShoppingCart,OrderInfo,OrderGoods
from .serializers import UserShopingCartSerializer,UserCartDetailSerializer,OrderSerializer,OrderDetailSerializer

class ShopingCartViewset(viewsets.ModelViewSet):
    """
    购物车功能
    list:
        获取购物车详情
    create:
        加入购物车
    delete:
        删除购物车记录
    """
    lookup_field = "goods_id"
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = UserShopingCartSerializer
    authentication_classes = (JSONWebTokenAuthentication,authentication.SessionAuthentication)
    def get_queryset(self): #只能查看自己的购物记录
        return ShoppingCart.objects.filter(user=self.request.user)
    def get_serializer_class(self):
        """
        用户action不同，序列化不同
        """
        if self.action == "list":
            return UserCartDetailSerializer
        return UserShopingCartSerializer

class OrderViewSet(mixins.ListModelMixin,mixins.DestroyModelMixin,mixins.CreateModelMixin,\
                   mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    """
    订单管理:
    list:
        获取个人订单
    delete:
        删除订单
    create:
        创建订单
    """

    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = OrderSerializer
    authentication_classes = (JSONWebTokenAuthentication,authentication.SessionAuthentication)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return OrderDetailSerializer
        else:
            return OrderSerializer
    def get_queryset(self): #只能查看自己的购物记录
        return OrderInfo.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        order = serializer.save()
        shop_carts = ShoppingCart.objects.filter(user =self.request.user)
        for shop_cart in  shop_carts:
            order_goods = OrderGoods()
            order_goods.goods = shop_cart.goods
            order_goods.goods_num = shop_cart.nums
            order_goods.order = order
            order_goods.save()
            shop_carts.delete()
        return order


from rest_framework.views import APIView
from utils.alipay import AliPay
from fish_site.settings import ali_pub_key_path,private_key_path
from rest_framework.response import  Response

class AlipayView(APIView):
    def get(self,request):
        """
        处理支付宝的return_url 返回
        :param request:
        :return:
        """
        process_dict ={}
        for key,valuse in request.GET.items():
            process_dict[key] = valuse
        sign = process_dict.pop('sign',None)

        alipay = AliPay(
            appid="2016091700534234",
            app_notify_url="http://101.132.194.31:8000/alipay/return/",
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,  沙箱环境用True
            return_url="http://101.132.194.31:8000/alipay/return/"
        )

        verfy_result = alipay.verify(process_dict, sign)
        if verfy_result:
            order_sn = process_dict.get('out_trade_no',None)
            trade_no = process_dict.get('trade_no',None)
            trade_status = process_dict.get('trade_status')

            existed_orders = OrderInfo.objects.filter(order_sn=order_sn)
            for existed_order in existed_orders:
                existed_order.pay_status = trade_status
                existed_order.trade_no = trade_no
                existed_order.pay_time = datetime.now()
                existed_order.save()

            response = redirect('index')
            response.set_cookie("nextPath","pay",max_age=30)
            return response

            #return Response("success")
        else:
            response = redirect('index')
            return response
    def post(self,request):
        """
        处理支付宝的notify_url
        :param request:
        :return:
        """
        process_dict ={}
        for key,valuse in request.POST.items():
            process_dict[key] = valuse
        sign = process_dict.pop('sign',None)

        alipay = AliPay(
            appid="2016091700534234",
            app_notify_url="http://101.132.194.31:8000/alipay/return/",
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,  沙箱环境用True
            return_url="http://101.132.194.31:8000/alipay/return/"
        )

        verfy_result = alipay.verify(process_dict, sign)
        if verfy_result:
            order_sn = process_dict.get('out_trade_no',None)
            trade_no = process_dict.get('trade_no',None)
            trade_status = process_dict.get('trade_status')

            existed_orders = OrderInfo.objects.filter(order_sn=order_sn)
            for existed_order in existed_orders:
                existed_order.pay_status = trade_status
                existed_order.trade_no = trade_no
                existed_order.pay_time = datetime.now()
                existed_order.save()

            return Response("success")





