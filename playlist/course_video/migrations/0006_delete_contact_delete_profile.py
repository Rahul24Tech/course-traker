# Generated by Django 4.1.3 on 2023-01-17 16:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("course_video", "0005_playlistitem_watch_later_playlist"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Contact",
        ),
        migrations.DeleteModel(
            name="Profile",
        ),
    ]