from django.shortcuts import render

# Create your views here.

from  django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model  #获取用户方式二
from django.db.models import Q
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .serializers import VerifyCodeSerializer,UserRegSerializer
from utils.sms_send import AliYunSMS
from string import digits
from random import sample
from json import dumps,loads
from users.models import VerifyCode
from rest_framework_jwt.serializers import jwt_encode_handler,jwt_payload_handler


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


class UserViewset(mixins.CreateModelMixin,viewsets.GenericViewSet):
    """
    创建用户
    """
    serializer_class = UserRegSerializer
    queryset = User.objects.all()


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

    def perform_create(self, serializer):
        return serializer.save()