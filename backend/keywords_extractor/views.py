from rest_framework import generics
from .models import Keyword
from .serializers import KeywordSerializer


class KeywordCreateAPIView(generics.CreateAPIView):
    queryset = Keyword.objects.all()
    serializer_class = KeywordSerializer


class KeywordListAPIView(generics.ListAPIView):
    queryset = Keyword.objects.all()
    serializer_class = KeywordSerializer


class KeywordRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Keyword.objects.all()
    serializer_class = KeywordSerializer
    lookup_field = "main_keyword"


class KeywordDestroyAPIView(generics.DestroyAPIView):
    queryset = Keyword.objects.all()
    serializer_class = KeywordSerializer
    lookup_field = "main_keyword"
