# Generated by Django 4.1.2 on 2022-10-15 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("convert", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="fileupload",
            name="image_name",
            field=models.CharField(default="None", max_length=200),
        ),
    ]
