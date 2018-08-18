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
from django.conf.urls import url,include
from django.contrib import admin
import xadmin
from fish_site.settings import MEDIA_ROOT
from django.views.static import serve
# from goods.view_base import GoodsListView
from goods.views import GoodsListViewSet,GoodsCategoryViewSet
from users.views import SmsCustomViewset,UserViewset
from user_operation.views import UserFavViewset
from  rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from  rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token

# 创建路由器并注册我们的视图。
router = DefaultRouter()
router.register(r'goods', GoodsListViewSet)  #url 路径 goods
router.register(r'categorys',GoodsCategoryViewSet)
router.register(r'sms',SmsCustomViewset,base_name='codes')
router.register('users',UserViewset,base_name='users')
#收藏
router.register('userfavs',UserFavViewset,base_name="userfavs")


# GoodsCategoryViewSet.as_view(
#     {"get":list},
# )



urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r"^media/(?P<path>.*)$", serve, {"document_root":MEDIA_ROOT}),

    url(r'^', include(router.urls)),

    url(r'^api-auth/', include('rest_framework.urls')),
    #DRF 自带认证模式
    url(r'^api-token-auth/', views.obtain_auth_token),
    url(r'docs/',include_docs_urls(title='fish shop api')),

    #REST framework JWT Auth
    url(r'^login/', obtain_jwt_token),

]
