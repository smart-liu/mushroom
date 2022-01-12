

from rest_framework import serializers

from emergency.models import Building


class EmergencyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        exclude = ("id", "type", "create_time")


class EmergencyDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = "__all__"
