# Generated by Django 4.2.9 on 2024-01-30 22:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("sensor", "0002_alter_airpollution_value"),
    ]

    operations = [
        migrations.AddField(
            model_name="airpollution",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="images/"),
        ),
    ]