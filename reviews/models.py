from django.db import models

class Review(models.Model):
    review_text = models.TextField()
    rating = models.IntegerField()
    sentiment = models.CharField(max_length=10)

