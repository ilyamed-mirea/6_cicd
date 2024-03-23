from rest_enumfield import EnumField
from rest_framework import serializers
from app.models import Answer


class GetAnswerQuerySerializer(serializers.Serializer):
    question = serializers.StringRelatedField
    answer_message = serializers.StringRelatedField
    answer_file = serializers.StringRelatedField | None


class NewApplicationSerializer(serializers.Serializer):
    user_id = serializers.UUIDField()
    start = serializers.CharField()
    finish = serializers.CharField()

    def create(self, validated_data):
        return Application(
            validated_data["user_id"], validated_data["start"], validated_data["finish"]
        )


class ApplicationDetailsSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    status = EnumField(choices=ApplicationStatuses)
    start = serializers.CharField()
    finish = serializers.CharField()
    created_date = serializers.DateTimeField()
