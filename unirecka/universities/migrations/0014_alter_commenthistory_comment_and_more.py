# Generated by Django 4.2.2 on 2023-09-28 05:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "universities",
            "0013_alter_commenthistory_comment_alter_review_title_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="commenthistory",
            name="comment",
            field=models.ForeignKey(
                blank=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="universities.comment",
            ),
        ),
        migrations.AlterField(
            model_name="reviewhistory",
            name="review",
            field=models.ForeignKey(
                blank=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="universities.review",
            ),
        ),
    ]
