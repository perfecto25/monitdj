# Generated by Django 4.2.5 on 2024-01-09 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0012_agent_cycle"),
    ]

    operations = [
        migrations.AddField(
            model_name="service",
            name="last_modified",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
