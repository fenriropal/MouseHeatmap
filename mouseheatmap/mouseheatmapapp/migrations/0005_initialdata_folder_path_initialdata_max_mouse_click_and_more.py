# Generated by Django 4.1.1 on 2022-10-06 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mouseheatmapapp", "0004_initialdata_pub_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="initialdata",
            name="folder_path",
            field=models.FilePathField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="initialdata",
            name="max_mouse_click",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="initialdata",
            name="max_mouse_movement",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="initialdata",
            name="min_mouse_click",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="initialdata",
            name="min_mouse_movement",
            field=models.IntegerField(default=0),
        ),
    ]