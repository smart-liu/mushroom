from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication

from django.db.models import Q

from forum.models import Topic, Community
from user_operation.serializer import UserTopicRetrieveSerializer, UserTopicListSerializer, \
    UserCreateTopicSerializer, UserUpdateTopicSerializer, UserRetrieveCommunitySerializer, UserListCommunitySerializer, \
    UserCreateCommunitySerializer, UserUpdateCommunitySerializer


class UserOperationPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 100


class UserTopicListViewSet(ModelViewSet):
    """
    list:
        获取用户发布的帖子
    read:
        获取发布帖子详细信息
    create:
        创建帖子
    update:
        更新用户帖子信息
    delete：
        删除用户帖子
    """
    pagination_class = UserOperationPagination
    ordering_fields = ("-create_time", )
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "list":
            return UserTopicListSerializer
        elif self.action == "create":
            return UserCreateTopicSerializer
        elif self.action == "update" or self.action == "partial_update":
            return UserUpdateTopicSerializer
        return UserTopicRetrieveSerializer

    def get_queryset(self):
        return Topic.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        return serializer.save()


class UserCommunityViewSet(ModelViewSet):
    """
    list:
        获取用户加入的或创建的社区
    read:
        获取社区详细信息
    create:
        用户创建社区
    update:
        更新用户社区信息
    delete：
        删除用户社区
    """
    pagination_class = UserOperationPagination
    ordering_fields = ("-create_time", )
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "list":
            return UserListCommunitySerializer
        elif self.action == "create":
            return UserCreateCommunitySerializer
        elif self.action == "update" or self.action == "partial_update":
            return UserUpdateCommunitySerializer
        return UserRetrieveCommunitySerializer

    def get_queryset(self):
        return Community.objects.filter(Q(user=self.request.user) | Q(is_common=True))

    def perform_create(self, serializer):
        return serializer.save()
