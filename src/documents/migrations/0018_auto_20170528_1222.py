# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-28 12:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0017_auto_20170528_1216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='sentence',
            field=models.CharField(max_length=160, null=True),
        ),
    ]
