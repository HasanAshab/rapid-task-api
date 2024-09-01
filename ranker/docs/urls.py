from django.urls import path
from drf_spectacular.views import (
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from .views import SchemaView

urlpatterns = [
    path("docs/schema/", SchemaView.as_view(), name="schema"),
    path(
        "docs/ui/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "docs/ui/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]
