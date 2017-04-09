# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-08 14:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('siprof', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='permissions',
            name='azienda',
            field=models.CharField(default='asc', max_length=10, verbose_name="Azienda su cui l'utente sta operando."),
            preserve_default=False,
        ),
    ]
