# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-06 14:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('district', models.CharField(default='', max_length=100, verbose_name='区域')),
                ('address', models.CharField(default='', max_length=100, verbose_name='详细地址')),
                ('signer_name', models.CharField(default='', max_length=30, verbose_name='签受人')),
                ('signer_mobile', models.CharField(default='', max_length=11, verbose_name='电话')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '用户收货地址',
                'verbose_name_plural': '用户收货地址',
            },
        ),
        migrations.CreateModel(
            name='UserFav',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '用户收藏',
                'verbose_name_plural': '用户收藏',
            },
        ),
        migrations.CreateModel(
            name='UserLevingMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message_type', models.IntegerField(choices=[(1, '留言'), (2, '投诉'), (3, '询问'), (4, '售后'), (5, '求购')], default=1, help_text='留言类型 1(留言)2(投诉)3(询问)4(售后)5(求购)', verbose_name='留言类型')),
                ('subject', models.CharField(default='', help_text='主题', max_length=100, verbose_name='主题')),
                ('message', models.TextField(default='', help_text='留言内容', verbose_name='留言内容')),
                ('file', models.FileField(help_text='上传文件', upload_to='', verbose_name='上传文件')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '用户留言',
                'verbose_name_plural': '用户留言',
            },
        ),
    ]
