# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-28 10:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0011_auto_20161125_1907'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='drawing',
            field=models.ImageField(default='', upload_to='drawings/'),
            preserve_default=False,
        ),
    ]
