from django.db import models
from users.models import CustomUser


class URL(models.Model):
    """URL class"""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    url = models.CharField(max_length=500)
    title_exist = models.BooleanField(blank=True)
    title_length = models.IntegerField(blank=True)
    description_exist = models.BooleanField(blank=True)
    h1_exist = models.BooleanField(blank=True)
    h_tags_order = models.BooleanField(blank=True)
    h1_count = models.IntegerField(blank=True)
    img_alt = models.BooleanField(blank=True)
    key_words = models.JSONField(blank=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
