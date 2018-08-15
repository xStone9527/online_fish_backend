from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser

class UserProfile(AbstractUser):
    """
    用户
    """
    ROLE_STYLE = ((0,u"未知"),(1,u"队员"),(2,u"队长"),(3,u"评委"))
    # name = models.CharField(max_length=30,null=True,blank=True,verbose_name=u'姓名')
    role = models.IntegerField(choices=ROLE_STYLE,default=0,verbose_name=u"角色",help_text=u"如需修改，获取更多权限，请联系管理员")
    birthday = models.DateField(null=True,blank=True,verbose_name=u"出生年月日")
    mobile = models.CharField(null=True,blank=True,max_length=11,verbose_name='电话')
    genger = models.CharField(max_length=6,choices=(("male",u'男'),("female",u'女')),default='male')


    class Meta:
        #db_table = "user"
        verbose_name = u'用户信息'
        verbose_name_plural = verbose_name
    def __unicode__(self):
        return "账号:"+self.username+" 姓名:"+self.last_name + self.first_name

class VerifyCode(models.Model):
    code = models.CharField(max_length=10,verbose_name="验证码")
    mobile = models.CharField(max_length=11,verbose_name='电话')
    add_time = models.DateTimeField(default=datetime.now,verbose_name='添加时间')


    class Meta:
        verbose_name = '短信验证码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return  self.code