# -*- coding: utf-8 -*-

__author__ = 'xl'
"""
__date__ = TIME： 2018/07/07 上午11:31
describe:
"""
import sys
import os
pwd = os.path.dirname(os.path.realpath(__file__))
print(pwd)
sys.path.append(pwd+"../")  #添加到 manage.py 同级目录
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fish_site.settings")
import django
django.setup()

from goods.models import Goods,GoodsCategory,GoodsImage
from db_tool.data.product_data import row_data

print(len(row_data))
# for goods_detail in row_data:
#
#     good_instance = Goods()
#     good_instance.name = goods_detail['name']
#     good_instance.market_price = float(goods_detail['market_price'].replace("元","").replace("￥",""))
#     good_instance.shop_price = float(goods_detail['sale_price'].replace("元","").replace("￥",""))
#     good_instance.goods_brief = goods_detail['desc'] if goods_detail["desc"] else ""
#     good_instance.goods_desc = goods_detail['goods_desc'] if goods_detail["goods_desc"] else ""
#     good_instance.goods_front_image = goods_detail["images"][0] if  goods_detail['images'] else ""
#     print(goods_detail['categorys'][-1])
#     good_instance.category = GoodsCategory.objects.get(name=goods_detail['categorys'][-1])
#     good_instance.save()
#
#     for index ,image in enumerate(goods_detail['images']):
#         goods_image = GoodsImage()
#         goods_image.goods = good_instance
#         goods_image.image = image
#         goods_image.index = index
#         goods_image.save()





