# Generated by Django 5.0.7 on 2024-07-23 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0028_hostgroup_id_alter_hostgroup_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hostgroup',
            name='host',
            field=models.ManyToManyField(blank=True, to='main.host'),
        ),
    ]