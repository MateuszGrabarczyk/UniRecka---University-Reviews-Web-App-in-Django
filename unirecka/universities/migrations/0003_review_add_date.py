# Generated by Django 4.2.2 on 2023-07-02 07:04

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('universities', '0002_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='add_date',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
    ]