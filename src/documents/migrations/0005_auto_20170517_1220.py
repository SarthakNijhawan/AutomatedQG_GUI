# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-17 12:20
from __future__ import unicode_literals

from django.db import migrations, models
import documents.models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0004_auto_20170517_1045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='unprocessed_doc',
            field=models.FileField(blank=True, null=True, upload_to=documents.models.upload_location_unprocessed_file),
        ),
    ]