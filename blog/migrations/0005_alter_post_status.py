# Generated by Django 5.1.5 on 2025-02-13 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0004_alter_post_published_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="status",
            field=models.BooleanField(default=True),
        ),
    ]
