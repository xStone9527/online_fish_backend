# -*- coding: utf-8 -*-

__author__ = 'xl'
"""
__date__ = TIME： 2018/07/19 下午8:26
describe:
"""
from .models import  VerifyCode
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model  #获取用户方式二
from datetime import datetime,timedelta

#
import re
#
User = get_user_model()
REGEX_MOBILE = "^((1[3,5,8][0-9])|(14[5,7])|(17[0,6,7,8])|(19[7]))\\d{8}$"

class VerifyCodeSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11,min_length=11,required=True,help_text="手机号码")

    def validate_mobile(self,mobile):
        # 验证用户是否存在
        if User.objects.filter(mobile =mobile).count():
            raise serializers.ValidationError("用户已经存在")
        # 验证手机号码
        if not re.match(REGEX_MOBILE,mobile):
            raise  serializers.ValidationError("手机号码格式不正确")
        #验证短信发送频率
        one_minutes_ago = datetime.now() -timedelta(hours=0,minutes=1,seconds=0)
        if VerifyCode.objects.filter(add_time__lt=one_minutes_ago,mobile=mobile).count():
            raise  serializers.ValidationError("具体上次发送未超过60S")
        return mobile


class UserRegSerializer(serializers.ModelSerializer):
    code = serializers.CharField(max_length=4,min_length=4,required=True,error_messages={
        "max_length":"验证码格式错误",
        "min_length":"验证码格式错误",
        "required":"未输入验证码",
        "blank":"请输入验证码",
    },help_text="验证码",label="验证码",write_only=True)
    username = serializers.CharField(required=True,allow_blank=False,
                                     validators=[UniqueValidator(queryset=User.objects.all(),message="用户已经存在")],label="账号")
    password = serializers.CharField(style={'input_type': 'password'},label="密码",write_only=True)
    mobile = serializers.CharField(allow_blank=True,required=False)

    def validate_code(self,code):
        verify_records = VerifyCode.objects.filter(mobile=self.initial_data['username']).order_by('-add_time')
        if verify_records:
            verify_lastest = verify_records[0]
            if verify_lastest.code != code:
                serializers.ValidationError("验证码错误")
            five_minutes_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
            if five_minutes_ago > verify_lastest.add_time:
                serializers.ValidationError("验证码过期")
        else:
            raise  serializers.ValidationError("没有验证码记录")
        #此处没必要return code 因为code不需要保存
    def validate(self, attrs):
        attrs['mobile'] = attrs['username']
        del attrs["code"]
        return  attrs
    class Meta:
        model = User
        fields = ("username","mobile","password","code")

    # def create(self, validated_data):
    #     user = super(UserRegSerializer,self).create(validated_data=validated_data)
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     return user
class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model =User
        fields = ("name", "gender", "birthday", "email","mobile")





