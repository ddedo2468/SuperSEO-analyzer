from rest_framework.response import Response
from .models import URL
from .serializers import UrlSerializer
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .utils import analyze_url


class UrlCreateAPIView(generics.CreateAPIView):
    """create a new url instance"""

    serializer_class = UrlSerializer
    permission_classes = [IsAuthenticated]

    # Handle the case when the request limit reached for certain url

    def get_queryset(self):
        user = self.request.user
        return URL.objects.filter(owner=user)

    def perform_create(self, serializer):
        # analyze the current url and save the result
        url = self.request.data.get("url")
        if not url:
            raise serializers.ValidationError({"error": "URL is required"})

        analysis_result = analyze_url(url)

        serializer.save(owner=self.request.user, **analysis_result)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(response.data, status=status.HTTP_201_CREATED)


class UrlListAPIView(generics.ListAPIView):
    """List urls instances"""

    serializer_class = UrlSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return URL.objects.filter(owner=user)


class UrlRetrieveAPIView(generics.RetrieveAPIView):
    """retrive a certain istance of URL"""

    serializer_class = UrlSerializer
    lookup_field = "url"

    def get_queryset(self):
        user = self.request.user
        return URL.objects.filter(owner=user)


class UrlDestroyAPIView(generics.DestroyAPIView):
    """destroy a certain istance of URL"""

    serializer_class = UrlSerializer
    lookup_field = "url"

    def get_queryset(self):
        user = self.request.user
        return URL.objects.filter(owner=user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Deleted"}, status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()
