# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-17 10:06
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasker', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserPermissions',
            new_name='Permissions',
        ),
    ]
