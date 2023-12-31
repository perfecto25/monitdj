# Generated by Django 4.2.5 on 2023-09-26 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0006_agent_state"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="service",
            name="unique_match",
        ),
        migrations.AddConstraint(
            model_name="agent",
            constraint=models.UniqueConstraint(
                fields=("name",), name="unique_agent_name"
            ),
        ),
        migrations.AddConstraint(
            model_name="service",
            constraint=models.UniqueConstraint(
                fields=("name", "agent"), name="unique_svc_name"
            ),
        ),
    ]
