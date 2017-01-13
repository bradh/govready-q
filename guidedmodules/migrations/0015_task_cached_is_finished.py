# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-06 18:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guidedmodules', '0014_taskanswerhistory_stored_encoding'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='cached_is_finished',
            field=models.NullBooleanField(help_text='Cached value storing whether the Task is finished.'),
        ),
    ]