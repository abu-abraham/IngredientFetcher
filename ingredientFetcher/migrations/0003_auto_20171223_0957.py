# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-23 09:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ingredientFetcher', '0002_useractivity'),
    ]

    operations = [
        migrations.AddField(
            model_name='useractivity',
            name='context',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='useractivity',
            name='lastActive',
            field=models.DateField(null=True),
        ),
    ]