from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    """用户"""
    id = models.AutoField(primary_key=True)
    nick_name = models.CharField(max_length=30, null=True, blank=True, verbose_name="姓名")
    real_name = models.CharField(max_length=50, default="", verbose_name="真实姓名")
    birthday = models.DateField(null=True, blank=True, verbose_name="出生日期")
    gender = models.CharField(max_length=6, choices=(("male", "男"), ("female", "女")), default="男")
    mobile = models.CharField(max_length=11, verbose_name="电话")
    password = models.CharField(max_length=128, verbose_name="登录密码")
    wechat = models.CharField(max_length=50, verbose_name="微信账号", default='')
    avatar = models.CharField(max_length=150, default='', verbose_name="头像OSS-URL")
    signature = models.CharField(max_length=50, default="", verbose_name="个性签名")
    email = models.CharField(max_length=254, default="", verbose_name="电子邮件")
    allow_post = models.BooleanField(default=True, verbose_name="是否禁言")
    open_id = models.CharField(max_length=32, verbose_name="微信登录使用")
    last_login = models.DateTimeField(verbose_name='最近一次登录时间', default=datetime.now)
    create_time = models.DateTimeField(verbose_name='注册时间', default=datetime.now)
    update_time = models.DateTimeField(verbose_name='更新时间', default=datetime.now)

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class VerifyCode(models.Model):
    """
    短信验证码
    """
    code = models.CharField(max_length=10, verbose_name="验证码")
    mobile = models.CharField(max_length=11, verbose_name="电话")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "短信验证码"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code


class UserAddress(models.Model):
    """用户地址"""
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, related_name="address", on_delete=models.CASCADE, verbose_name="用户id")
    province_code = models.CharField(max_length=10, default='', verbose_name="前端使用--省份的code")
    city_code = models.CharField(max_length=10, default='', verbose_name="前端使用--市的code")
    county_code = models.CharField(max_length=10, default='', verbose_name="前端使用--区、县的code")
    location = models.CharField(max_length=100, default='', verbose_name="位置信息")
    signer_name = models.CharField(max_length=100, default="", verbose_name="签收人")
    signer_mobile = models.CharField(max_length=11, default="", verbose_name="电话")
    is_default = models.BooleanField(default=False, verbose_name="是否设置默认")
    create_time = models.DateTimeField(verbose_name='创建时间', default=datetime.now)
    update_time = models.DateTimeField(verbose_name='更新时间', default=datetime.now)

    class Meta:
        verbose_name = "用户地址"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.location


class UserCompany(models.Model):
    """用户公司"""
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, related_name="company", on_delete=models.CASCADE, verbose_name="用户id")
    name = models.CharField(max_length=50, verbose_name="所在公司名称", default='')
    duties = models.CharField(max_length=50, verbose_name="部门职务", default='')
    expertise = models.CharField(max_length=50, verbose_name="业务专长", default='')
    qualifications = models.CharField(max_length=50, verbose_name="资质信息", default='')
    create_time = models.DateTimeField(verbose_name='创建时间', default=datetime.now)
    update_time = models.DateTimeField(verbose_name='更新时间', default=datetime.now)

    class Meta:
        verbose_name = "用户公司"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
