# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-08 06:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_auto_20171208_0530'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(default='/static/img/default_flower_image.png', upload_to=''),
        ),
    ]