from rest_framework import serializers
from .models import Keyword
from .utils import search_and_extract_keywords
import asyncio
from datetime import timedelta
from django.utils import timezone


class KeywordSerializer(serializers.ModelSerializer):


    class Meta:
        model = Keyword
        fields = ["id", "main_keyword", "results", "created_at", "updated_at"]

    def create(self, validated_data):
        main_keyword = validated_data.get("main_keyword")

        # Check if the keyword already exists
        try:
            existing_keyword = Keyword.objects.get(main_keyword=main_keyword)
            one_month_ago = timezone.now() - timedelta(days=30)

            if existing_keyword.updated_at > one_month_ago:
                # Return existing keyword if updated recently
                return existing_keyword
            else:
                # Perform a new analysis if the existing keyword is older than one month
                new_results = asyncio.run(search_and_extract_keywords(main_keyword))

                if not new_results:
                    raise serializers.ValidationError(
                        "No results found for the keyword."
                    )

                existing_keyword.results = new_results
                existing_keyword.save()

                return existing_keyword
        except Keyword.DoesNotExist:
            # If keyword does not exist, create a new one
            new_results = asyncio.run(search_and_extract_keywords(main_keyword))

            if not new_results:
                raise serializers.ValidationError("No results found for the keyword.")

            new_keyword = Keyword.objects.create(
                main_keyword=main_keyword, results=new_results
            )
            return new_keyword
