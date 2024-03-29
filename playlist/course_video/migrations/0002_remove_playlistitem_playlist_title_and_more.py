# Generated by Django 4.1.3 on 2023-01-11 05:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("course_video", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="playlistitem",
            name="playlist_title",
        ),
        migrations.AddField(
            model_name="playlistitem",
            name="playlist",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="course_video.course",
            ),
            preserve_default=False,
        ),
    ]
