# Generated by Django 4.1.1 on 2022-09-29 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mouseheatmapapp", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="HeatmapInfo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("min_duration_time", models.IntegerField(default=0)),
                ("max_duration_time", models.IntegerField(default=0)),
            ],
        ),
    ]