# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-07 01:08
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('goods', '0002_goodscategorybrand_category'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderGoods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goods_sum', models.IntegerField(default=0, verbose_name='商品数量')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('goods', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.Goods', verbose_name='商品')),
            ],
        ),
        migrations.CreateModel(
            name='OrderInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_sn', models.CharField(max_length=30, verbose_name='订单号')),
                ('trande_no', models.CharField(blank=True, max_length=100, null=True, unique=True, verbose_name='订单号')),
                ('pay_status', models.CharField(choices=[('suceesee', '成功'), ('cancel', '取消'), ('wait_pay', '待支付')], max_length=30, verbose_name='订单状态')),
                ('pay_script', models.CharField(max_length=200, verbose_name='订单留言')),
                ('order_mount', models.FloatField(default=0.0, verbose_name='订单金额')),
                ('pay_time', models.DateTimeField(auto_now_add=True, verbose_name='订单时间')),
                ('address', models.CharField(default='', max_length=100, verbose_name='收货地址')),
                ('signer_name', models.CharField(max_length=30, verbose_name='签收人')),
                ('signer_mobile', models.CharField(max_length=11, verbose_name='签收人电话')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '订单',
                'verbose_name_plural': '订单',
            },
        ),
        migrations.CreateModel(
            name='ShoppingCart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num', models.IntegerField(default=0, verbose_name='购买数量')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('goods', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.Goods', verbose_name='商品')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '购物车',
                'verbose_name_plural': '购物车',
            },
        ),
        migrations.AddField(
            model_name='ordergoods',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trade.OrderInfo', verbose_name='订单信息'),
        ),
    ]
