# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-25 19:22
from __future__ import unicode_literals

import django.core.files.storage
from django.db import migrations, models
import sifilesmanager.models


class Migration(migrations.Migration):

    dependencies = [
        ('sifilesmanager', '0005_auto_20170322_1448'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sifile',
            name='filename',
            field=models.FileField(storage=django.core.files.storage.FileSystemStorage(location='C:\\Seafile\\Py\\si\\si\\data'), upload_to=sifilesmanager.models.upload_to_sha1),
        ),
    ]
