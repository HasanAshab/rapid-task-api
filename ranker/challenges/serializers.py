from rest_framework import serializers
from .models import Challenge, ChallengeStep
from ranker.difficulties.models import Difficulty


class ChallengeDifficultySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Difficulty
        fields = "__all__"
        read_only_fields = (
            "name",
            "slug",
            "score",
            "xp_value",
            "xp_penalty",
            "light_color",
            "dark_color",
        )


class ChallengeSerializer(serializers.ModelSerializer):
    difficulty = ChallengeDifficultySerializer()

    class Meta:
        model = Challenge
        fields = (
            "id",
            "title",
            "status",
            "repeat_type",
            "snooze_for_today",
            "is_pinned",
            "due_date",
            "difficulty",
            "order",
            "ignore_for_ai",
        )

    def validate(self, data):
        difficulty_id = data.pop("difficulty", {}).get("id")
        if difficulty_id:
            data["difficulty_id"] = difficulty_id
        return data


class GroupedChallengeSerializer(serializers.Serializer):
    group = serializers.CharField()
    challenges = serializers.ListField(child=ChallengeSerializer())


class ChallengeDifficultyCountSerializer(serializers.ModelSerializer):
    challenge_count = serializers.IntegerField()

    class Meta:
        model = Difficulty
        fields = "__all__"


class CompletedChallengeActivitiesSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    difficulties = ChallengeDifficultyCountSerializer(many=True)


class ChallengeActivitiesSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    failed = serializers.IntegerField()
    completed = CompletedChallengeActivitiesSerializer()


class ReOrderingSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    order = serializers.IntegerField(min_value=0)


class ChallengeStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChallengeStep
        fields = (
            "id",
            "title",
            "is_completed",
            "order",
        )


class ChallengeSuggestionSerializer(serializers.ModelSerializer):
    difficulty = ChallengeDifficultySerializer()

    class Meta:
        model = Challenge
        fields = (
            "title",
            "difficulty",
        )
