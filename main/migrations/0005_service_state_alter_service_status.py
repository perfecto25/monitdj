# Generated by Django 4.2.5 on 2023-09-26 05:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_service_data_alter_service_monitor_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='state',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='service',
            name='status',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
