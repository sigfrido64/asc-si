# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-22 14:48
from __future__ import unicode_literals

import django.core.files.storage
from django.db import migrations, models
import sifilesmanager.models


class Migration(migrations.Migration):

    dependencies = [
        ('sifilesmanager', '0004_auto_20170317_1006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sifile',
            name='filename',
            field=models.FileField(storage=django.core.files.storage.FileSystemStorage(location='D:\\Seafile\\Py\\si\\si\\data'), upload_to=sifilesmanager.models.upload_to_sha1),
        ),
    ]
