# Generated by Django 4.1.3 on 2023-01-08 12:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("course_video", "0007_alter_profile_time_left"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="profile",
            name="time_left",
        ),
    ]
