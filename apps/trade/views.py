from django.shortcuts import render

# Create your views here.
import time
import string
import random

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

