# Generated by Django 4.2.5 on 2023-10-12 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_agent_last_checkin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ack',
            name='last_modified',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='agent',
            name='last_checkin',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
