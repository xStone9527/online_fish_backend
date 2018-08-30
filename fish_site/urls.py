"""fish_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

import xadmin
from django.views.static import serve
from django.conf.urls import url,include
from django.contrib import admin
from django.views.generic import TemplateView
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token

from fish_site.settings import MEDIA_ROOT
# from goods.view_base import GoodsListView
from goods.views import GoodsListViewSet,GoodsCategoryViewSet,BannerViewset,IndexCategoryViewSet
from users.views import SmsCustomViewset,UserViewset
from user_operation.views import UserFavViewset,UserMessageViewset,AddressViewset
from trade.views import ShopingCartViewset,OrderViewSet,AlipayView

# 创建路由器并注册我们的视图。
router = DefaultRouter()
router.register(r'goods', GoodsListViewSet)  #url 路径 goods
router.register(r'categorys',GoodsCategoryViewSet)
router.register(r'sms',SmsCustomViewset,base_name='codes')
router.register('users',UserViewset,base_name='users')
#收藏
router.register('userfavs',UserFavViewset,base_name="userfavs")
#用户留言
router.register('messages',UserMessageViewset,base_name='userleavemsg')
#收获地址
router.register("address",AddressViewset,base_name="address")
#购物车
router.register("shopcarts",ShopingCartViewset,base_name="shopcarts")
#订单相关
router.register("orders",OrderViewSet,base_name="orders")
#轮播图
router.register('banners',BannerViewset,base_name="banners")
#首页商品系列数据
router.register('indexgoods',IndexCategoryViewSet,base_name="indexgoods")

# GoodsCategoryViewSet.as_view(
#     {"get":list},
# )



urlpatterns = [
    url(r'^index/',TemplateView.as_view(template_name='index.html'),name='index'),

    url(r'^xadmin/', xadmin.site.urls),
    url(r"^media/(?P<path>.*)$", serve, {"document_root":MEDIA_ROOT}),

    url(r'^', include(router.urls)),

    url(r'^api-auth/', include('rest_framework.urls')),
    #DRF 自带认证模式
    url(r'^api-token-auth/', views.obtain_auth_token),
    url(r'docs/',include_docs_urls(title='api文档在线')),

    #REST framework JWT Auth
    url(r'^login/', obtain_jwt_token),

    url('^alipay/return/',AlipayView.as_view(),name="alipay"),



]
