from django.db import models

class Review(models.Model):
    review_text = models.TextField()
    rating = models.FloatField(null=True, blank=True)  # Изменено на FloatField и добавлены null=True, blank=True
    sentiment = models.CharField(max_length=10, null=True, blank=True)  # Добавлены null=True, blank=True
