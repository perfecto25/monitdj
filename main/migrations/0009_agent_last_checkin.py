# Generated by Django 4.2.5 on 2023-10-12 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_ack'),
    ]

    operations = [
        migrations.AddField(
            model_name='agent',
            name='last_checkin',
            field=models.DateField(blank=True, null=True),
        ),
    ]
