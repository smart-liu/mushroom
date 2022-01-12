from rest_framework import serializers

from forum.models import Topic, Community, CommunityUsers, TopicComment, CommunityCard
from users.models import User, UserAddress, UserCompany


class AddressSerializer(serializers.ModelSerializer):
    """用户地址"""

    class Meta:
        model = UserAddress
        exclude = ("user", "update_time", "signer_name", "signer_mobile")


class CompanySerializer(serializers.ModelSerializer):
    """用户公司"""

    class Meta:
        model = UserCompany
        fields = ("name", "duties", "expertise", "qualifications", "create_time")


class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户详情序列化类
    """
    address = AddressSerializer(many=True)
    company = CompanySerializer()

    class Meta:
        model = User
        fields = ("id", "nick_name", "gender", "mobile", "avatar", "address", "company")


class TopicListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ("title", "content", "views", "comments", "thumbs", "create_time")


class TopicDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ("title", "content", "views", "comments", "thumbs", "create_time")


class CommunityTopicDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = "__all__"


class CommunityTopicListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        exclude = ("update_time", "community", "hidden", "user")


class CommunityMembersListSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer()

    class Meta:
        model = CommunityUsers
        fields = "__all__"


class CommunityMembersDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityUsers
        fields = ('id', )


class CommunityMembersUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityUsers
        fields = "__all__"
        read_only_fields = ("create_time", "user", "community")


class CommunityMembersCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityUsers
        fields = "__all__"
        read_only_fields = ("create_time", "is_admin", "allow_post", "user")

    def validate(self, attrs):
        """校验用户是否在该社区"""
        user = self.context["request"].user
        community_user = CommunityUsers.objects.filter(user=user)
        if community_user:
            raise serializers.ValidationError("已加入该社区")
        return attrs

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return CommunityUsers.objects.create(**validated_data)


class TopicThumbUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Topic
        fields = ("id", "thumbs")
        read_only_fields = ("thumbs", )


class TopicCommentRetrieveSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer()

    class Meta:
        model = TopicComment
        fields = "__all__"


class TopicCommentCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = TopicComment
        fields = ("topic", "content", "parent_comment")


class CommunityCardDetailSerializer(serializers.ModelSerializer):
    apply_user = UserDetailSerializer()
    receive_user = UserDetailSerializer()

    class Meta:
        model = CommunityCard
        fields = "__all__"


class CommunityCardCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityCard
        fields = ("apply_user", "receive_user", "status", "count")
        read_only_fields = ("count", )


class CommunityCardUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityCard
        fields = ("status", )