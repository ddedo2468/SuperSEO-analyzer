from django.urls import path
from .views import (
    KeywordCreateAPIView,
    KeywordListAPIView,
    KeywordRetrieveAPIView,
    KeywordDestroyAPIView,
)

urlpatterns = [
    path("create/", KeywordCreateAPIView.as_view(), name="keyword-create"),
    path("", KeywordListAPIView.as_view(), name="keyword-list"),
    path(
        "<str:main_keyword>", KeywordRetrieveAPIView.as_view(), name="keyword-retrieve"
    ),
    path(
        "delete/<str:main_keyword>/",
        KeywordDestroyAPIView.as_view(),
        name="keyword-delete",
    ),
]
