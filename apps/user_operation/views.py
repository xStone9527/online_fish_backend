from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets,mixins,permissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication

from .models import UserFav,UserLeavingMessage,UserAddress
from .serializers import UserFavSerializer,UserFavDetailSerializer,UserLeavingMessageSerializer,UserAddressSerializer
from .permissions import IsOwnerOrReadOnly



class UserFavViewset(mixins.CreateModelMixin,mixins.DestroyModelMixin,mixins.ListModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    """
    用户收藏功能
    list:
        "用户收藏列表"
    create:
        "创建收藏"
    destory:
        "删除收藏"
    """
    #queryset = UserFav.objects.all()
    serializer_class = UserFavSerializer
    permission_classes = (permissions.IsAuthenticated,IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication,SessionAuthentication)
    lookup_field = "goods_id"  #用户进入页面 按照商品编号查找收藏记录

    def get_queryset(self): #只能查看自己的收藏
        return UserFav.objects.filter(user=self.request.user)
    def get_serializer_class(self):
        """
        用户action不同，序列化不同
        """
        if self.action == "list":
            return UserFavDetailSerializer
        elif self.action == "create":
            return UserFavSerializer
        return UserFavSerializer
class UserMessageViewset(mixins.CreateModelMixin,mixins.DestroyModelMixin,mixins.ListModelMixin,\
                         viewsets.GenericViewSet):
    """
    list:
        获取用户留言
    create:
        创建用户留言
    destory:
        删除用户留言
    """
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = UserLeavingMessageSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    def get_queryset(self): #只能查看自己的收藏
        return UserLeavingMessage.objects.filter(user=self.request.user)

#class AddressViewset(mixins.ListModelMixin,mixins.CreateModelMixin,mixins.DestroyModelMixin,mixins.UpdateModelMixin,viewsets.GenericViewSet)
# 替换成 ModelViewSet 已经包含了 增删改查
class AddressViewset(viewsets.ModelViewSet):
    """
    list:
        获取收货地址
    create:
        创建收货地址
    update:
        更新收货地址
    delete:
        删除收货地址
    """
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = UserAddressSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    def get_queryset(self): #只能查看自己的收货地址
        return UserAddress.objects.filter(user=self.request.user)

