import random

from rest_framework import filters
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.pagination import PageNumberPagination
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import SessionAuthentication
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, ListModelMixin, UpdateModelMixin
from rest_framework import status as drf_status

from forum.filter import TopicFilter, CommunityUsersFilter
from forum.models import Topic, CommunityUsers, TopicComment, CommunityCard
from forum.permissions import IsCommunityAdminPermission
from forum.serializer import TopicListSerializer, TopicDetailSerializer, CommunityTopicDetailSerializer, \
    CommunityTopicListSerializer, CommunityMembersListSerializer, CommunityMembersCreateSerializer, \
    CommunityMembersUpdateSerializer, CommunityMembersDeleteSerializer, TopicThumbUpdateSerializer, \
    TopicCommentCreateSerializer, TopicCommentRetrieveSerializer, CommunityCardCreateSerializer, \
    CommunityCardDetailSerializer, CommunityCardUpdateSerializer


class CommonPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 100


class CommunityDetailViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    """
    retrieve: 首页帖子详情
    list: 首页帖子列表
    """
    queryset = Topic.objects.all()
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = TopicFilter
    pagination_class = CommonPagination
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = [IsAuthenticated]
    search_fields = ("title", "content")
    ordering_fields = ("create_time",)

    def get_serializer_class(self):
        if self.action == "list":
            return CommunityTopicListSerializer
        return CommunityTopicDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        views_random = random.randint(1, 10)
        instance.views += views_random
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, drf_status.HTTP_200_OK)


class CommunityMembersViewSet(ModelViewSet):
    """
    read:
        获取成员信息
    list:
        获取社区成员
    create:
        加入社区
    update:
        更改社区成员信息(社区管理员权限)
    delete:
        删除社区成员(社区管理员权限)
    """
    queryset = CommunityUsers.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    # permission_classes = [IsAuthenticated]
    pagination_class = CommonPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = CommunityUsersFilter
    # search_fields = ("community", )
    ordering_fields = ("create_time",)

    def get_permissions(self):
        """更新社区成员时，设置权限"""
        if self.action not in ["create", "retrieve"]:
            return [IsAuthenticated(), IsCommunityAdminPermission()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == "create":
            return CommunityMembersCreateSerializer
        elif self.action == "update" or self.action == "partial_update":
            return CommunityMembersUpdateSerializer
        elif self.action == "delete":
            return CommunityMembersDeleteSerializer
        return CommunityMembersListSerializer


class TopicThumbViewSet(UpdateModelMixin, GenericViewSet):
    """
    update:
        帖子点赞
    """
    queryset = Topic.objects.all()
    serializer_class = TopicThumbUpdateSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.thumbs += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, drf_status.HTTP_202_ACCEPTED)


class TopicCommentViewSet(CreateModelMixin, RetrieveModelMixin, GenericViewSet):
    """
    retrieve:
        获取评论
    create:
        帖子评论
    """
    queryset = TopicComment.objects.all()
    serializer_class = TopicCommentCreateSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return TopicCommentRetrieveSerializer
        return TopicCommentCreateSerializer

    def create(self, request, *args, **kwargs):
        json_data = request.data
        json_data["user"] = request.user
        serializer = self.get_serializer(json_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        # 帖子评论数+1
        topic = Topic.objects.get(request.data["topic"])
        topic.comments += 1
        topic.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=drf_status.HTTP_201_CREATED, headers=headers)


class CommunityCardChangeViewSet(ModelViewSet):
    """
    list:
        获取我的名片
    retrieve:
        获取名片详情
    create:
        申请交换名片
    update:
        审核名片
    """
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = [IsAuthenticated]
    pagination_class = CommonPagination

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return CommunityCardDetailSerializer
        elif self.action == "create":
            return CommunityCardCreateSerializer
        return CommunityCardUpdateSerializer

    def get_queryset(self):
        queryset = CommunityCard.objects.all()
        if self.action == "list":
            queryset = CommunityCard.objects.filter(status=1)
        return queryset
