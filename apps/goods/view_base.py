# -*- coding: utf-8 -*-

__author__ = 'xl'
"""
__date__ = TIME： 2018/07/08 上午8:10
describe:
"""
from  django.views.generic import ListView
from  django.views.generic import View
from  django.http import HttpResponse,JsonResponse
import json
from  .models import Goods

class GoodsListView(View):
    def get(self,request):
        goods = Goods.objects.all() #此时并没有调用数据库
        goods_list = []

        #方式一 自己添加各个Field
        # for good in goods:
        #     json_dict = {}
        #     json_dict['name'] = good.name
        #     json_dict['market_price'] = good.market_price
        #     goods_list.append(json_dict)
        # return HttpResponse(json.dumps(goods_list),content_type="application/json")

        #方式二 利用 Django z自带 model ==》 dict 转化
        # from django.forms.models import model_to_dict
        #
        # for good in goods:
        #     good_dict = model_to_dict(good)
        #     goods_list.append(good_dict)
        # return HttpResponse(json.dumps(goods_list),content_type="application/json")

        #方式三 Django 利用自带 serializers
        # from django.core import serializers
        #
        # json_data = serializers.serialize('json',goods)
        # return  HttpResponse(json_data,content_type='application/json')


        #方式四 不使用HttpResponse 使用 JsonResponse
        #HttpResponse 参数为json型数据
        #JsonResponse 参数 为json型对象 并讲safe 设置为 False
        from django.core import serializers

        json_data = serializers.serialize('json',goods)
        json_dict = json.loads(json_data)
        return  JsonResponse(json_dict,safe=False)

