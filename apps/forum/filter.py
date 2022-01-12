import django_filters

from forum.models import Topic, CommunityUsers


class TopicFilter(django_filters.rest_framework.FilterSet):
    """帖子过滤器"""
    community = django_filters.NumberFilter(field_name="community", help_text="社区id")
    # title = django_filters.CharFilter(field_name="title", help_text="帖子标题", lookup_expr="icontains")

    class Meta:
        model = Topic
        fields = ("community", )


class CommunityUsersFilter(django_filters.rest_framework.FilterSet):
    """帖子成员过滤器"""
    community = django_filters.NumberFilter(field_name="community", help_text="社区id")

    class Meta:
        model = CommunityUsers
        fields = ("community", )
