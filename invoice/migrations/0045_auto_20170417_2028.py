# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-04-17 12:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0044_product_is_wardrobe'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='Black_White',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='product',
            name='Cherry_White',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='product',
            name='Walnut_White',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='invoiceproduct',
            name='color',
            field=models.CharField(choices=[(b'R', '\u7d05\u6afb\u6843'), (b'B', '\u9ed1\u6a61'), (b'BW', '\u9ed1\u6a61/\u767d'), (b'CW', '\u7d05\u6afb\u6843/\u767d'), (b'W', '\u767d\u6728\u7d0b'), (b'L', '\u6dfa\u80e1\u6843'), (b'WW', '\u6dfa\u80e1\u6843/\u767d'), (b'GC', '\u9999\u6ab3\u4eae\u5149'), (b'C', '\u9999\u6ab3\u6728\u7d0b'), (b'M', '\u6953\u6728'), (b'A', '\u6a61\u6728'), (b'G', '\u767d\u4eae\u5149'), (b'O', '\u5176\u4ed6')], default=b'O', max_length=2),
        ),
    ]