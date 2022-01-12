from datetime import datetime

from django.db import models

from forum.models import Community


class Building(models.Model):
    id = models.AutoField(primary_key=True)
    community = models.ForeignKey(Community, related_name="community_building", on_delete=models.CASCADE)
    type = models.IntegerField(default=0, verbose_name="建筑类型，0-社区应急通道")
    name = models.CharField(null=False, blank=False, max_length=255, verbose_name="建筑名称")
    property_phone = models.CharField(null=False, blank=False, max_length=20, verbose_name="物业电话")
    police_phone = models.CharField(max_length=20, default="", verbose_name="派出所电话")
    fire_phone = models.CharField(max_length=20, default="", verbose_name="消防电话")
    address = models.CharField(null=False, blank=False, max_length=255, verbose_name="地址")
    image = models.CharField(max_length=255, default="", verbose_name="建筑图片")
    alarm_info = models.CharField(null=False, blank=False, max_length=255, verbose_name="警告内容")
    create_time = models.DateTimeField(default=datetime.now, verbose_name="创建时间")


class EmergencyChannel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name="逃生通道名称，一般以楼层命名")
    image = models.CharField(max_length=255, verbose_name="逃生通道一览图")
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name="emergency_channel")
    create_time = models.DateTimeField(default=datetime.now, verbose_name="创建时间")
