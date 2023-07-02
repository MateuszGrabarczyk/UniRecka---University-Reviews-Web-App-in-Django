from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
class University(models.Model):
    name = models.CharField(max_length=150)
    voivodeship = models.CharField(max_length=150)
    city = models.CharField(max_length=150)
    link = models.CharField(max_length=150)
    class Meta:
        verbose_name = 'University'
        verbose_name_plural = 'Universities'

class Review(models.Model):
    title = models.CharField( max_length=150)
    description = models.CharField( max_length=150)
    rating = models.IntegerField(validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ])
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'