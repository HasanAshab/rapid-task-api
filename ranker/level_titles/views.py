from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import LevelTitle
from .serializers import LevelTitleListSerializer
from .pagination import LevelTitlePagination


class LevelTitlesView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = LevelTitle.objects.all()
    serializer_class = LevelTitleListSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = {
        "required_level": ["gt"],
    }
    ordering_fields = ["required_level"]
    ordering = ["required_level"]
    pagination_class = LevelTitlePagination
