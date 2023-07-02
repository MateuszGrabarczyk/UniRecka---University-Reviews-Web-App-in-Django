from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from django.contrib.auth.models import User
class University(models.Model):
    name = models.CharField(max_length=150)
    voivodeship = models.CharField(max_length=150)
    city = models.CharField(max_length=150)
    link = models.CharField(max_length=150)
    class Meta:
        verbose_name = 'University'
        verbose_name_plural = 'Universities'

    def __str__(self):
        return f"{self.name}"

class Review(models.Model):
    title = models.CharField( max_length=150)
    description = models.CharField( max_length=150)
    rating = models.IntegerField(validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ])
    add_date = models.DateTimeField(default=timezone.now, blank=True)
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'

    def __str__(self):
        return f"{self.title}"
