# Generated by Django 4.2.2 on 2023-07-03 11:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('universities', '0003_review_add_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReviewReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=150)),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='universities.review')),
            ],
            options={
                'verbose_name': 'ReviewReport',
                'verbose_name_plural': 'ReviewReports',
            },
        ),
    ]
