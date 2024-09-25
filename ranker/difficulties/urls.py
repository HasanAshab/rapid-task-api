from django.urls import path
from .views import (
    DifficultiesView,
    DifficultyView,
    DifficultySuggestionView,
)

urlpatterns = [
    path("difficulties/", DifficultiesView.as_view(), name="difficulties"),
    path(
        "difficulty/suggestions",
        DifficultySuggestionView.as_view(),
        name="difficulty_suggestion",
    ),
    path(
        "difficulties/<int:pk>/", DifficultyView.as_view(), name="difficulty"
    ),
]
