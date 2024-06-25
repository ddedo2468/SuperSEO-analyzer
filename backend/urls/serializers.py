from rest_framework import serializers
from .models import URL
from urls.utils import analyze_url


class UrlSerializer(serializers.ModelSerializer):
    """class to serialize url model"""

    class Meta:
        model = URL
        fields = [
            "url",
            "title_exist",
            "title_length",
            "description_exist",
            "h1_exist",
            "h_tags_order",
            "h1_count",
            "img_alt",
            "key_words",
        ]

    def create(self, validated_data):
        """
        Create a new URL instance.
        If the URL already exists, update it instead.
        """
        url = validated_data.get("url")
        owner = validated_data.get("owner")
        existing_url = URL.objects.filter(url=url, owner=owner).first()

        if existing_url:
            for attr, value in validated_data.items():
                setattr(existing_url, attr, value)
            existing_url.save()
            return existing_url

        return URL.objects.create(**validated_data)
