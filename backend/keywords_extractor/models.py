from django.db import models


class Keyword(models.Model):
    """KEYWORDS Class"""

    main_keyword = models.CharField(max_length=120)
    results = models.JSONField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.main_keyword
