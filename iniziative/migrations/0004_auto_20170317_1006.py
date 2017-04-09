# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-17 10:06
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iniziative', '0003_auto_20170309_1359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='iniziativa',
            name='cup_cig',
            field=models.CharField(blank=True, max_length=80, verbose_name='CIG/CUP se presente'),
        ),
        migrations.AlterField(
            model_name='iniziativa',
            name='descrizione',
            field=models.CharField(max_length=80, validators=[django.core.validators.MinLengthValidator(5)], verbose_name="Breve descrizione dell'iniziativa"),
        ),
        migrations.AlterField(
            model_name='iniziativa',
            name='in_uso',
            field=models.BooleanField(db_index=True, default=True, verbose_name="L'iniziativa è tutt'ora in uso ?"),
        ),
        migrations.AlterField(
            model_name='iniziativa',
            name='iva_scaricabile',
            field=models.BooleanField(db_index=True, default=True, verbose_name="L'IVA delle spese connesse all'iniziativa è scaricabile ?"),
        ),
        migrations.AlterField(
            model_name='iniziativa',
            name='nome',
            field=models.CharField(db_index=True, max_length=80, unique=True, validators=[django.core.validators.MinLengthValidator(3)], verbose_name="Nome dell'iniziativa"),
        ),
    ]
