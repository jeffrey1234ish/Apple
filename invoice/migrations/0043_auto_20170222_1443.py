# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-22 06:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0042_auto_20170221_1829'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='Glossy_White',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='invoiceproduct',
            name='color',
            field=models.CharField(choices=[(b'R', '\u7d05\u6afb\u6843'), (b'B', '\u9ed1\u6a61'), (b'W', '\u767d\u6728\u7d0b'), (b'L', '\u6dfa\u80e1\u6843'), (b'M', '\u6953\u6728'), (b'A', '\u6a61\u6728'), (b'G', '\u767d\u4eae\u5149'), (b'O', '\u5176\u4ed6')], default=b'O', max_length=1),
        ),
    ]
