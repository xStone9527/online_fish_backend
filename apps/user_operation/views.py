from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets,mixins,permissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication

from .models import UserFav
from .serializers import UserFavSerializer
from .permissions import IsOwnerOrReadOnly



class UserFavViewset(mixins.CreateModelMixin,mixins.DestroyModelMixin,mixins.ListModelMixin,viewsets.GenericViewSet):
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

    def get_queryset(self): #只能查看自己的收藏
        return UserFav.objects.filter(user=self.request.user)

