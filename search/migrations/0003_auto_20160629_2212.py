# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-29 14:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0002_stockinfo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockhistoryinfo',
            name='StockID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='search.StockInfo'),
        ),
    ]