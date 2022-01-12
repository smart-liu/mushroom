from rest_framework import serializers

from forum.models import Topic, Community, CommunityUsers


class UserTopicRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ("title", "views", "comments", "thumbs", "create_time")


class UserTopicListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ("id", "title", "views", "comments", "thumbs", "create_time")


class UserUpdateTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ("title", "content")


class UserCreateTopicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Topic
        fields = ("title", "content", "community", "create_time")
        read_only_fields = ("create_time", )

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return Topic.objects.create(**validated_data)


class CommunityUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityUsers
        fields = ("is_admin", "allow_post", "create_time")


class UserRetrieveCommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = ("name", "announcement", "type", "create_time")


class UserListCommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = ("id", "name", "announcement", "type", "create_time")


class UserUpdateCommunitySerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False, allow_null=True, label="社区名称")

    class Meta:
        model = Community
        fields = ("name", "announcement")

    def validate(self, attrs):
        if "name" not in attrs and "announcement" not in attrs:
            raise serializers.ValidationError("one of name or announcement is required")
        return attrs


class UserCreateCommunitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Community
        fields = ("name", "announcement", "avatar", "type", "create_time")
        read_only_fields = ("create_time", "type")

    def create(self, validated_data):
        create_user = self.context["request"].user
        validated_data["user"] = create_user
        community = Community.objects.create(**validated_data)
        # 将创建者加入到社区成员
        CommunityUsers.objects.create(**{"user": create_user, "community": community, "is_create": True, "is_admin": True})
        return community
