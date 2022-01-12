from datetime import datetime

from django.db import models

from users.models import User


class Community(models.Model):
    """社区"""
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, related_name="community", on_delete=models.CASCADE, verbose_name="创建社区的用户")
    name = models.CharField(max_length=128, null=False, blank=False, verbose_name="社区名称")
    avatar = models.CharField(max_length=256, null=False, blank=False, verbose_name="社区头像")
    announcement = models.CharField(max_length=256, default="", verbose_name="社区公告")
    type = models.SmallIntegerField(default=0, verbose_name="社区类型，0-虚拟兴趣社区 1-真实社区")
    is_common = models.BooleanField(default=False, verbose_name="是否为公共社区")
    create_time = models.DateTimeField(default=datetime.now, verbose_name="创建时间")
    update_time = models.DateTimeField(default=datetime.now, verbose_name="更新时间")

    class Meta:
        verbose_name = "社区"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CommunityUsers(models.Model):
    """社区成员"""
    id = models.AutoField(primary_key=True)
    community = models.ForeignKey(Community, related_name="community_users", on_delete=models.CASCADE, verbose_name="社区id")
    user = models.ForeignKey(User, related_name="user_communities", on_delete=models.CASCADE, verbose_name="社区id")
    is_create = models.BooleanField(default=False, verbose_name="是否为创建者")
    is_admin = models.BooleanField(default=False, verbose_name="该用户在该社区是否为管理员，管理员可删帖子，可禁言，可管理成员")
    allow_post = models.BooleanField(default=False, verbose_name="该用户是否在该社区被禁言")
    create_time = models.DateTimeField(default=datetime.now, verbose_name="用户加入社区时间")

    class Meta:
        verbose_name = "社区成员"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.name


class Topic(models.Model):
    """帖子"""
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, related_name="user_topic", on_delete=models.CASCADE, verbose_name="用户id")
    title = models.CharField(max_length=200, blank=False, verbose_name="帖子标题")
    content = models.TextField(null=True, verbose_name="帖子内容")
    views = models.IntegerField(default=0, verbose_name="帖子查看量")
    comments = models.IntegerField(default=0, verbose_name="回复数量")
    thumbs = models.IntegerField(default=0, verbose_name="点赞数量")
    hidden = models.BooleanField(default=False, verbose_name="是否屏蔽")
    level = models.IntegerField(default=0, verbose_name="排序级别")
    community = models.ForeignKey(Community, on_delete=models.CASCADE,
                                  related_name="community_topic", verbose_name="社区id")
    create_time = models.DateTimeField(default=datetime.now, verbose_name="创建时间")
    update_time = models.DateTimeField(default=datetime.now, verbose_name="更新时间")

    class Meta:
        verbose_name = "帖子"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class TopicComment(models.Model):
    """帖子评论"""
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, related_name="create_user", on_delete=models.CASCADE, verbose_name="创建评论用户")
    topic = models.ForeignKey(Topic, related_name="topic_comment", on_delete=models.CASCADE, verbose_name="帖子id")
    content = models.TextField(null=False, blank=False, verbose_name="评论内容")
    parent_comment = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE, verbose_name="父级评论")
    create_time = models.DateTimeField(default=datetime.now, verbose_name="评论时间")

    class Meta:
        verbose_name = "帖子评论"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.id


class Label(models.Model):
    """兴趣标签"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128, verbose_name="兴趣标签名称")
    desc = models.CharField(max_length=256, verbose_name="标签描述")

    class Meta:
        verbose_name = "兴趣标签"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CommunityLabel(models.Model):
    """社区兴趣标签"""
    id = models.AutoField(primary_key=True)
    community = models.ForeignKey(Community, related_name="community_labels", on_delete=models.CASCADE, verbose_name="社区id")
    label = models.ForeignKey(Label, related_name="label_communities", on_delete=models.CASCADE, verbose_name="兴趣标签id")

    class Meta:
        verbose_name = "社区兴趣标签"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.id


class CommunityCard(models.Model):
    """社区名片"""
    id = models.AutoField(primary_key=True)
    apply_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="apply_user", verbose_name="交换名片人id")
    receive_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receive_user", verbose_name="被交换人名片id")
    status = models.IntegerField(default=0, verbose_name="状态 0-等待被交换人同意交换 1-已同意交换名片 2-拒绝交换名片")
    count = models.IntegerField(default=3, verbose_name="交换名片计数 最大三次")
    create_time = models.DateTimeField(default=datetime.now, verbose_name="交换名片时间")
