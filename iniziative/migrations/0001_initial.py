# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Iniziativa',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(db_index=True, validators=[django.core.validators.MinLengthValidator(3)], max_length=80, unique=True, verbose_name='Nome Iniziativa')),
                ('descrizione', models.CharField(validators=[django.core.validators.MinLengthValidator(5)], max_length=80, verbose_name='Descrizione')),
                ('cup_cig', models.CharField(blank=True, max_length=80, verbose_name='CIG/CUP')),
                ('in_uso', models.BooleanField(db_index=True, default=True, verbose_name='In Uso')),
                ('data_aggiornamento', models.DateTimeField(auto_now=True)),
                ('data_creazione', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Iniziative',
                'verbose_name': 'Iniziativa',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Raggruppamento',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(db_index=True, max_length=80)),
                ('descrizione', models.CharField(max_length=80)),
                ('in_uso', models.BooleanField(db_index=True, default=True)),
                ('ordine', models.CharField(max_length=10)),
                ('data_aggiornamento', models.DateTimeField(auto_now=True)),
                ('data_creazione', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Raggruppamenti',
                'verbose_name': 'Raggruppamento',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SottoIniziativa',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(db_index=True, max_length=80)),
                ('descrizione', models.CharField(max_length=80)),
                ('in_uso', models.BooleanField(db_index=True, default=True)),
                ('data_aggiornamento', models.DateTimeField(auto_now=True)),
                ('data_creazione', models.DateTimeField(auto_now_add=True)),
                ('iniziativa', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='iniziative.Iniziativa')),
            ],
            options={
                'verbose_name_plural': 'Sotto Iniziative',
                'verbose_name': 'Sotto Iniziativa',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='raggruppamento',
            name='sotto_iniziativa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='iniziative.SottoIniziativa'),
            preserve_default=True,
        ),
    ]
