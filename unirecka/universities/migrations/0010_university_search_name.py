# Generated by Django 4.2.2 on 2023-07-10 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("universities", "0009_commentreport"),
    ]

    operations = [
        migrations.AddField(
            model_name="university",
            name="search_name",
            field=models.CharField(blank=True, max_length=150),
        ),
    ]
