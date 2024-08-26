from django.contrib.auth.models import User
from event import models
from rest_framework import serializers


class EventUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class EventSerializer(serializers.ModelSerializer):
    created_by = EventUserSerializer(read_only=True)
    attendees = EventUserSerializer(many=True, read_only=True)

    class Meta:
        model = models.Event
        fields = [
            "id",
            "name",
            "description",
            "start_date",
            "end_date",
            "capacity",
            "type",
            "attendees",
            "created_by",
        ]


class SuccessResponseSerializer(serializers.Serializer):
    detail = serializers.CharField()


class ErrorResponseSerializer(SuccessResponseSerializer):
    pass
