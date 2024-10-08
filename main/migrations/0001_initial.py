# Generated by Django 5.0.7 on 2024-09-24 12:47

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Connector',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=40)),
                ('ctype', models.CharField(choices=[('slack', 'slack'), ('email', 'email')], db_index=True, default='slack', max_length=25)),
                ('active', models.BooleanField(default=False)),
                ('webhook', models.CharField(blank=True, max_length=500, null=True)),
                ('smtp_server', models.CharField(blank=True, max_length=50, null=True)),
                ('smtp_port', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('monit_id', models.UUIDField(editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('state', models.IntegerField(blank=True, null=True)),
                ('last_checkin', models.DateTimeField(default=django.utils.timezone.now)),
                ('monit_version', models.CharField(blank=True, max_length=30, null=True)),
                ('uptime', models.IntegerField(blank=True, null=True)),
                ('os_name', models.CharField(blank=True, max_length=30, null=True)),
                ('os_release', models.CharField(blank=True, max_length=35, null=True)),
                ('os_version', models.CharField(blank=True, max_length=40, null=True)),
                ('os_arch', models.CharField(blank=True, max_length=15, null=True)),
                ('cpu', models.IntegerField(blank=True, null=True)),
                ('mem', models.IntegerField(blank=True, null=True)),
                ('swap', models.IntegerField(blank=True, null=True)),
                ('cycle', models.IntegerField(blank=True, null=True)),
                ('active', models.BooleanField(default=True)),
                ('approved', models.BooleanField(default=False)),
                ('ignore', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='HostGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, default='', max_length=40)),
                ('status', models.IntegerField(blank=True, null=True)),
                ('state', models.IntegerField(blank=True, null=True)),
                ('svc_type', models.IntegerField(blank=True, null=True)),
                ('monitor', models.IntegerField(blank=True, null=True)),
                ('event', models.CharField(blank=True, max_length=300, null=True)),
                ('data', models.JSONField(blank=True, null=True)),
                ('last_checkin', models.DateTimeField(default=django.utils.timezone.now)),
                ('ack', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.AddConstraint(
            model_name='connector',
            constraint=models.UniqueConstraint(fields=('name',), name='unique_connector_name'),
        ),
        migrations.AddConstraint(
            model_name='host',
            constraint=models.UniqueConstraint(fields=('monit_id',), name='unique_monit_id'),
        ),
        migrations.AddField(
            model_name='hostgroup',
            name='host',
            field=models.ManyToManyField(blank=True, to='main.host'),
        ),
        migrations.AddField(
            model_name='service',
            name='host',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service', to='main.host'),
        ),
        migrations.AddConstraint(
            model_name='hostgroup',
            constraint=models.UniqueConstraint(fields=('name',), name='unique_hostgroup_name'),
        ),
        migrations.AddConstraint(
            model_name='service',
            constraint=models.UniqueConstraint(fields=('name', 'host'), name='unique_svc_name'),
        ),
    ]
