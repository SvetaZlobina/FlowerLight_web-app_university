# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-08 09:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_auto_20171208_0602'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(default='img/default_flower_image.png', upload_to=''),
        ),
    ]
