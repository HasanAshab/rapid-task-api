from rest_framework.permissions import (
    IsAuthenticated,
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
)
from drf_spectacular.utils import extend_schema
from .utils import suggest_difficulty_for
from .models import Difficulty
from .serializers import (
    DifficultySerializer,
    ChallengeDifficultySuggestionSerializer,
)


class DifficultiesView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Difficulty.objects.all()
    serializer_class = DifficultySerializer


class DifficultyView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Difficulty.objects.all()
    serializer_class = DifficultySerializer


class DifficultySuggestionView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ChallengeDifficultySuggestionSerializer

    @extend_schema(
        responses={
            200: DifficultySerializer(),
        }
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        challenge_title = serializer.validated_data["title"]
        difficulty = suggest_difficulty_for(request.user, challenge_title)
        return Response(difficulty)
