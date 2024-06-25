from rest_framework import serializers
from .models import Keyword
from .utils import search_and_extract_keywords
import asyncio
from datetime import timedelta
from django.utils import timezone


class KeywordSerializer(serializers.ModelSerializer):
    """
    A serializer class for the Keyword model. This class is used to convert instances
    of the Keyword model to and from JSON format for API endpoints.

    The Keyword model has the following fields:
    - id: The primary key of the keyword entry.
    - main_keyword: The main keyword string that is being tracked.
    - results: The results of the keyword analysis (e.g., common trigrams).
    - created_at: The timestamp when the keyword entry was created.
    - updated_at: The timestamp when the keyword entry was last updated.
    """

    class Meta:
        model = Keyword
        fields = ["id", "main_keyword", "results", "created_at", "updated_at"]

    def create(self, validated_data):
        main_keyword = validated_data.get("main_keyword")
        print("Main keyword:", main_keyword)

        # Check if the keyword already exists
        try:
            existing_keyword = Keyword.objects.get(main_keyword=main_keyword)
            one_month_ago = timezone.now() - timedelta(days=30)
            print("Existing keyword found, updated at:", existing_keyword.updated_at)

            if existing_keyword.updated_at > one_month_ago:
                # Return existing keyword if updated recently
                print("Keyword updated recently, returning existing keyword.")
                return existing_keyword
            else:
                # Perform a new analysis if the existing keyword is older than one month
                print("Keyword is older than one month, performing new analysis.")
                new_results = asyncio.run(search_and_extract_keywords(main_keyword))

                if not new_results:
                    raise serializers.ValidationError(
                        "No results found for the keyword."
                    )

                existing_keyword.results = new_results
                existing_keyword.save()

                print("Keyword updated:", existing_keyword.results)
                return existing_keyword
        except Keyword.DoesNotExist:
            # If keyword does not exist, create a new one
            print("Keyword does not exist, performing analysis.")
            new_results = asyncio.run(search_and_extract_keywords(main_keyword))

            if not new_results:
                raise serializers.ValidationError("No results found for the keyword.")

            new_keyword = Keyword.objects.create(
                main_keyword=main_keyword, results=new_results
            )
            print("New keyword created:", new_keyword.results)
            return new_keyword
