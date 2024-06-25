from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/keywords/", include("keywords_extractor.urls")),
    path("api/", include("urls.urls")),
    path("users/", include("users.urls")),
]
