# Generated by Django 4.2.2 on 2023-07-03 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('universities', '0004_reviewreport'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='description',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='reviewreport',
            name='description',
            field=models.CharField(max_length=500),
        ),
    ]
