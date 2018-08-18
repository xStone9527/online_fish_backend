from django.shortcuts import render

# Create your views here.

from string import digits
from random import sample
from json import dumps,loads

from  django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model  #获取用户方式二
from django.db.models import Q
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework_jwt.serializers import jwt_encode_handler,jwt_payload_handler
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from users.models import VerifyCode
from .serializers import VerifyCodeSerializer,UserRegSerializer,UserDetailSerializer
from utils.sms_send import AliYunSMS



User = get_user_model()

class CustomBackend(ModelBackend):
    """
    自定义用户验证
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username)|Q(mobile = username))
            if user.check_password(password):
                return user
        except Exception as  e:
            return None

class SmsCustomViewset(mixins.CreateModelMixin,viewsets.GenericViewSet):
    """
    发送短信验证码
    """
    serializer_class = VerifyCodeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True) #遇到错误直接抛出异常
        mobile = serializer.data['mobile']
        sms = AliYunSMS()

        verification_code = "".join(sample(digits,4))
        params = dumps({"code":verification_code})
        res = loads(sms.send_sms('17625320452', "向磊", "SMS_139850253", params))
        if res["Code"] == "OK":
            VerifyCode.objects.create(mobile=mobile,code=verification_code)
            return  Response({"mobile":mobile},status=status.HTTP_201_CREATED)
        else:
            return Response({"mobile":res['Message']},status=status.HTTP_400_BAD_REQUEST)

class UserViewset(mixins.CreateModelMixin,mixins.UpdateModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):  #mixins.UpdateModelMixin, 带来两种action put 全更新 putch 部分更新
    """
    创建用户
    """
    serializer_class = UserRegSerializer
    queryset = User.objects.all()
    authentication_classes = (SessionAuthentication,JSONWebTokenAuthentication)


    def get_permissions(self):
        """
        注册用户 和 获取用户信息时 权限不同
        """
        if self.action == "retrieve":
            return [permissions.IsAuthenticated()]
        elif self.action == "create":
            return []
        return []
    def get_serializer_class(self):
        """
        用户action不同，序列化不同
        """
        if self.action == "retrieve":
            return UserDetailSerializer
        elif self.action == "create":
            return UserRegSerializer
        return UserDetailSerializer




    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer) #获得创建的 User

        re_dict =serializer.data #原本返回的数据
        payload =jwt_payload_handler(user)
        re_dict['token'] = jwt_encode_handler(payload) #原本返回的数据基础上加Token
        re_dict['name'] = user.name  if user.name else user.username
        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    def get_object(self): #用户虽然输入id，都只返回当前用户。
        return self.request.user

    def perform_create(self, serializer):
        return serializer.save()