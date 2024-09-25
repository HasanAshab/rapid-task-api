from rest_framework import serializers
from ranker.challenges.models import Challenge
from .models import Difficulty


class DifficultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Difficulty
        fields = "__all__"


class ChallengeDifficultySuggestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenge
        fields = ("title",)
