from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from drf_standardized_response.openapi.utils import standard_openapi_response
from .utils import generate_username
from .serializers import (
    ProfileSerializer,
    SuggestUsernameSerializer,
)


class ProfileView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user


class SuggestUsernameView(APIView):
    @extend_schema(
        parameters=[SuggestUsernameSerializer],
        responses={
            200: standard_openapi_response(
                "SuggestUsername",
                {"data": serializers.ListField(child=serializers.CharField())},
            ),
        },
    )
    def get(self, request):
        serializer = SuggestUsernameSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        prefix = serializer.validated_data.get("prefix")
        max_suggestions = serializer.validated_data["max_suggestions"]
        suggested_usernames = [
            generate_username(prefix)
            for _ in range(max_suggestions)
            if generate_username(prefix)
        ]
        return Response(suggested_usernames)
