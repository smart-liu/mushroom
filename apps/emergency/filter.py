import django_filters

from emergency.models import Building


class CommunityEmergencyFilter(django_filters.rest_framework.FilterSet):
    """社区应急疏散过滤器"""
    community = django_filters.NumberFilter(field_name="community", help_text="社区id")

    class Meta:
        model = Building
        fields = ("community", )