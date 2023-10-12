# Generated by Django 4.2.5 on 2023-10-12 12:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0007_remove_service_unique_match_agent_unique_agent_name_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Ack",
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
                ("state", models.BooleanField(default=False)),
                ("last_modified", models.DateField(blank=True, null=True)),
                (
                    "service",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="service_object",
                        to="main.service",
                    ),
                ),
            ],
        ),
    ]
