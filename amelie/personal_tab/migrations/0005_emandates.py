# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-04-25 18:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personal_tab', '0004_new_personal_tab'),
    ]

    operations = [
        migrations.AddField(
            model_name='authorization',
            name='emandate_status',
            field=models.CharField(blank=True, choices=[('Success', 'Success'), ('Cancelled', 'Cancelled'), ('Expired', 'Expired'), ('Failure', 'Failure'), ('Open', 'Open'), ('Pending', 'Pending')], max_length=191, null=True, verbose_name='eMandate Bank Status'),
        ),
        migrations.AddField(
            model_name='authorization',
            name='emandate_uuid',
            field=models.UUIDField(blank=True, null=True, unique=True, verbose_name='eMandate UUID'),
        ),
        migrations.AddField(
            model_name='authorizationtype',
            name='emandate',
            field=models.BooleanField(default=False, verbose_name='eMandate'),
        ),
    ]
