from django.urls import path
from . import views


urlpatterns = [
    path("create/", views.UrlCreateAPIView.as_view()),
    path("delete/<path:url>", views.UrlDestroyAPIView.as_view()),
    path("", views.UrlListAPIView.as_view()),
    path("<path:url>", views.UrlRetrieveAPIView.as_view()),
]
