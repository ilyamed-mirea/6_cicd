from rest_enumfield import EnumField
from rest_framework import serializers
from .models import Answer, AnswerStatuses, Operation


class AnswerSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    creation_date = serializers.DateTimeField()
    message = serializers.CharField()
    file = serializers.CharField(allow_null=True, required=False)
    status = serializers.CharField()


class QuestionAnswerSerializer(serializers.Serializer):
    question = serializers.CharField()
    answer = AnswerSerializer()


class AddQASerializer(serializers.Serializer):
    question = serializers.CharField()
    answer_message = serializers.CharField()
    answer_status = EnumField(choices=AnswerStatuses)

    def create(self, validated_data):
        return Answer(
            validated_data["question"],
            validated_data["answer_message"],
            validated_data["answer_status"],
        )


class GetAnswerSerializer(serializers.Serializer):
    question = serializers.CharField()
    user_id = serializers.UUIDField()


class MostFrequentQuestionsSerializer(serializers.Serializer):
    return_count = serializers.IntegerField(min_value=0)


class GetQuestionsByUsersSerializer(serializers.Serializer):
    filename = serializers.CharField()


class OperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operation
        fields = ["id", "created_at", "updated_at", "completed", "result"]
        read_only_fields = ["id", "created_at", "updated_at"]
