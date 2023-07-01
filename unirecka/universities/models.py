from django.db import models

class University(models.Model):
    name = models.CharField(max_length=150)
    voivodeship = models.CharField(max_length=150)
    city = models.CharField(max_length=150)
    link = models.CharField(max_length=150)
    class Meta:
        verbose_name = 'University'
        verbose_name_plural = 'Universities'

