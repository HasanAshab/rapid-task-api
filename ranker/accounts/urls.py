from django.urls import path
from .views import (
    ProfileView,
    SuggestUsernameView,
)


urlpatterns = [
    path(
        "account/",
        ProfileView.as_view(),
        name="profile",
    ),
    path(
        "account/suggest-username/",
        SuggestUsernameView.as_view(),
        name="suggest_username",
    ),
]
