# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-26 14:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GraphDisplay', '0008_auto_20170926_0917'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resultfile',
            name='file',
            field=models.FileField(upload_to='results/'),
        ),
    ]
