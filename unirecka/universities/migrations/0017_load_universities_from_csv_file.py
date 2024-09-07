# Import necessary libraries
import csv
import os

from django.db import migrations
from unidecode import unidecode

CSV_FILE_PATH = os.path.join(os.path.dirname(__file__), "zestawienie.csv")


def load_universities(apps, schema_editor):
    University = apps.get_model("universities", "University")
    with open(CSV_FILE_PATH, "r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            name = row["Nazwa instytucji"]
            search_name = unidecode(name)
            voivodeship = row["Województwo"]
            city = row["Adres - miasto"]
            link = row["Strona www"]

            University.objects.create(
                name=name,
                search_name=search_name,
                voivodeship=voivodeship,
                city=city,
                link=link,
            )


class Migration(migrations.Migration):

    dependencies = [
        ("universities", "0016_alter_commenthistory_comment_and_more"),
    ]

    operations = [
        migrations.RunPython(load_universities),
    ]
