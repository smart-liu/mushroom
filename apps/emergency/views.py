from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication

from emergency.models import Building
from emergency.serializer import EmergencyDetailSerializer, EmergencyCreateSerializer
from emergency.filter import CommunityEmergencyFilter


class CommonPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 100


class EmergencyBuildViewSet(ModelViewSet):
    queryset = Building.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = [IsAuthenticated]
    pagination_class = CommonPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = CommunityEmergencyFilter
    search_fields = ("name", )
    ordering_fields = ("create_time", )

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return EmergencyDetailSerializer
        return EmergencyCreateSerializer
