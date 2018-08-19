from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets,permissions,authentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from user_operation.permissions import IsOwnerOrReadOnly
from .models import ShoppingCart
from .serializers import UserShopingCartSerializer

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
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = UserShopingCartSerializer
    authentication_classes = (JSONWebTokenAuthentication,authentication.SessionAuthentication)
    def get_queryset(self): #只能查看自己的购物记录
        return ShoppingCart.objects.filter(user=self.request.user)