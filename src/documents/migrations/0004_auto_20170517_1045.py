# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-17 10:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0003_auto_20170517_0908'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='doc_text',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='unprocessed_doc',
            field=models.FileField(blank=True, null=True, upload_to=b''),
        ),
    ]
