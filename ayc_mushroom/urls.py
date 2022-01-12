"""ayc_mushroom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from rest_framework.authtoken import views
from rest_framework.documentation import include_docs_urls
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.routers import DefaultRouter

from emergency.views import EmergencyBuildViewSet
from user_operation.views import UserTopicListViewSet, UserCommunityViewSet
from users.views import UserViewset, SmsCodeViewset, UploadApiView, UserAddressViewSet
from forum.views import CommunityDetailViewSet, CommunityMembersViewSet, TopicThumbViewSet, TopicCommentViewSet, \
    CommunityCardChangeViewSet

router = DefaultRouter()

# 用户
router.register(r"users", UserViewset, basename="users")
# 验证码
router.register(r"code", SmsCodeViewset, basename="code")
# 用户地址
router.register(r"address", UserAddressViewSet, basename="user_address")
# 用户帖子
router.register(r"user/topic", UserTopicListViewSet, basename="user_topic")
# 用户社区
router.register(r"user/community", UserCommunityViewSet, basename="user_community")
# 首页帖子
router.register(r"topic", CommunityDetailViewSet, basename="topic")
# 帖子点赞
router.register(r"topic/thumb", TopicThumbViewSet, basename="topic_thumb")
# 帖子评论
router.register(r"topic/comment", TopicCommentViewSet, basename="topic_comment")
# 首页社区成员
router.register(r"community/members", CommunityMembersViewSet, basename="community_members")
# 社区成员交换名片
router.register(r"community/card", CommunityCardChangeViewSet, basename="community_card")
# 真实社区消防应急疏散
router.register(r"emergency", EmergencyBuildViewSet, basename="emergency")

urlpatterns = [
    path('ayc_mushroom/admin/', admin.site.urls),  # 后台管理系统
    url(r'ayc_mushroom/api-auth/', include('rest_framework.urls', namespace="rest_framework")),  # REST framework的登录注销视图
    url(r'ayc_mushroom/docs/', include_docs_urls(title="蘑菇社区")),  # 后台api文档
    url(r'ayc_mushroom/api-token-auth/', views.obtain_auth_token),  # drf自带的token认证模式
    # 业务路由
    url(r"ayc_mushroom/login/", obtain_jwt_token),  # jwt-token登录
    url(r"ayc_mushroom/oss/", UploadApiView.as_view()),  # oss 文件上传 删除
    url(r"^ayc_mushroom/api-v1/", include(router.urls))
]
