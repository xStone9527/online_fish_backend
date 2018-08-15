# -*- coding: utf-8 -*-
import sys
from aliyunsdkdysmsapi.request.v20170525 import SendSmsRequest
# from aliyunsdkdysmsapi.request.v20170525 import QuerySendDetailsRequest
from aliyunsdkcore.client import AcsClient
import uuid
from aliyunsdkcore.profile import region_provider
# from aliyunsdkcore.http import method_type as MT
# from aliyunsdkcore.http import format_type as FT
from fish_site.settings import ALIYUN
from json import dumps
from random import randint

"""
短信业务调用接口示例，版本号：v20170525

Created on 2017-06-12

"""

# 注意：不要更改
REGION = "cn-hangzhou"
PRODUCT_NAME = "Dysmsapi"
DOMAIN = "dysmsapi.aliyuncs.com"

# acs_client = AcsClient(ALIYUN['SMS']["ACCESS_KEY_ID"], ALIYUN['SMS']['ACCESS_KEY_SECRET'], REGION)
# region_provider.add_endpoint(PRODUCT_NAME, REGION, DOMAIN)

# def send_sms(business_id, phone_numbers, sign_name, template_code, template_param=None):
#     smsRequest = SendSmsRequest.SendSmsRequest()
#     # 申请的短信模板编码,必填
#     smsRequest.set_TemplateCode(template_code)
#
#     # 短信模板变量参数
#     if template_param is not None:
#         smsRequest.set_TemplateParam(template_param)
#
#     # 设置业务请求流水号，必填。
#     smsRequest.set_OutId(business_id)
#
#     # 短信签名
#     smsRequest.set_SignName(sign_name)
#
#     # 数据提交方式
# 	# smsRequest.set_method(MT.POST)
#
# 	# 数据提交格式
#     # smsRequest.set_accept_format(FT.JSON)
#
#     # 短信发送的号码列表，必填。
#     smsRequest.set_PhoneNumbers(phone_numbers)
#
#     # 调用短信发送接口，返回json
#     smsResponse = acs_client.do_action_with_exception(smsRequest)
#
#     # TODO 业务处理
#
#     return smsResponse



# if __name__ == '__main__':
#     __business_id = uuid.uuid1()
#
#     params = "{\"code\":\"6666\"}"
#
#     print(send_sms(__business_id, "17625320452", "向磊", "SMS_139850253", params))
   
    
class AliYunSMS(object):
    def __init__(self,access_key_id=ALIYUN['SMS']["ACCESS_KEY_ID"],access_key_secret = ALIYUN['SMS']['ACCESS_KEY_SECRET']):

        self.acs_client = AcsClient(access_key_id, access_key_secret, REGION)
        region_provider.add_endpoint(PRODUCT_NAME, REGION, DOMAIN)

    def send_sms(self, phone_numbers, sign_name, template_code, template_param=None):
        smsRequest = SendSmsRequest.SendSmsRequest()
        # 申请的短信模板编码,必填
        smsRequest.set_TemplateCode(template_code)

        # 短信模板变量参数
        if template_param is not None:
            smsRequest.set_TemplateParam(template_param)

        # 设置业务请求流水号，必填。

        smsRequest.set_OutId(uuid.uuid1())

        # 短信签名
        smsRequest.set_SignName(sign_name)

        # 数据提交方式
        # smsRequest.set_method(MT.POST)

        # 数据提交格式
        # smsRequest.set_accept_format(FT.JSON)

        # 短信发送的号码列表，必填。
        smsRequest.set_PhoneNumbers(phone_numbers)

        # 调用短信发送接口，返回json
        smsResponse = self.acs_client.do_action_with_exception(smsRequest)

        # TODO 业务处理

        return smsResponse


if __name__ == '__main__':

    aliyunsms = AliYunSMS()
    params = '{"code":"6667"}'
    params = dumps({"code": str(randint(0, 9999))})
    # print(aliyunsms.send_sms('17625320452',"向磊", "SMS_139850253", params))


    #
    # print(send_sms( "17625320452", "向磊", "SMS_139850253", params))