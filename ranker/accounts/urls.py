from django.urls import path
from .views import (
    ProfileView,
)


urlpatterns = [
    path(
        "account/",
        ProfileView.as_view(),
        name="profile",
    ),
]
