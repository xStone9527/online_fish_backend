from django.db import models
from  users.models import UserProfile  #获取User用户方式一

# Create your models here.
from goods.models import Goods

from django.contrib.auth import get_user_model  #获取用户方式二
User = get_user_model()


class ShoppingCart(models.Model):
    user = models.ForeignKey(UserProfile,verbose_name="用户")
    goods = models.ForeignKey(Goods,verbose_name="商品")
    nums = models.IntegerField(default=0,verbose_name="购买数量")
    add_time = models.DateTimeField(auto_now_add=True,verbose_name="添加时间")

    class Meta:
        unique_together =("user","goods")
        verbose_name = "购物车"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s(%d)".format(self.goods.name,self.nums)


class OrderInfo(models.Model):

    """
    订单
    """
    ORDER_STATUS = (
        ("suceesee","成功"),
        ("cancel","取消"),
        ("wait_pay","待支付"),
    )


    user = models.ForeignKey(User,verbose_name="用户")
    order_sn = models.CharField(max_length=30,verbose_name="订单号")
    # nonce_str = models.CharField(max_length=50,null=True,blank=True,verbose_name="随机字符串")
    trade_no = models.CharField(max_length=100,unique=True,null=True,blank=True,verbose_name="订单号")
    pay_status = models.CharField(choices=ORDER_STATUS,max_length=30,verbose_name="订单状态")
    post_script = models.CharField(max_length=200,verbose_name="订单留言")
    order_mount = models.FloatField(default=0.0,verbose_name="订单金额")
    pay_time = models.DateTimeField(auto_now_add=True,verbose_name="订单时间")

    # 用户信息
    address = models.CharField(max_length=100,default="",verbose_name="收货地址")
    signer_name = models.CharField(max_length=30,verbose_name="签收人")
    signer_mobile = models.CharField(max_length=11,verbose_name="签收人电话")

    add_time = models.DateTimeField(auto_now_add=True,verbose_name="添加时间")

    class Meta:
        verbose_name = "订单"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.order_sn


class OrderGoods(models.Model):
    """
    订单商品详情
    """
    order = models.ForeignKey(OrderInfo,verbose_name="订单信息")
    goods = models.ForeignKey(Goods,verbose_name='商品')
    goods_sum = models.IntegerField(default=0,verbose_name="商品数量")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")

    class Mete:
        verbose_name = "订单商品"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.order.order_sn