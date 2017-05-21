# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-19 14:01
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('invoice', '0040_auto_20170219_1930'),
    ]

    operations = [
        migrations.AddField(
            model_name='sales',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='invoiceproduct',
            name='color',
            field=models.CharField(choices=[(b'R', '\u7d05\u6afb\u6843'), (b'B', '\u9ed1\u6a61'), (b'W', '\u767d\u6728\u7d0b'), (b'L', '\u6dfa\u80e1\u6843'), (b'M', '\u6953\u6728'), (b'A', '\u6a61\u6728'), (b'O', '\u5176\u4ed6')], default=b'O', max_length=1),
        ),
    ]
