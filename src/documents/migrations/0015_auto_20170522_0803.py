# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-22 08:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0014_question_hint'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='title',
            field=models.CharField(max_length=30),
        ),
    ]