from rest_framework import serializers
from ranker.users.models import User
from ranker.users.mixins import UserAvatarLinkSerializerMixin
from ranker.level_titles.serializers import LevelTitleSerializer


class ProfileSerializer(
    UserAvatarLinkSerializerMixin,
    serializers.ModelSerializer,
):
    level_title = LevelTitleSerializer(read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "is_email_verified",
            "username",
            "name",
            "age",
            "gender",
            "avatar",
            "date_joined",
            "is_superuser",
            "is_staff",
            "total_xp",
            "level",
            "level_title",
            "rank",
            "links",
        )
        read_only_fields = (
            "date_joined",
            "last_login",
            "email",
            "is_active",
            "is_staff",
            "is_superuser",
            "phone_number",
            "total_xp",
            "rank",
        )
        extra_kwargs = {"avatar": {"write_only": True}}
