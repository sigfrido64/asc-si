# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-01 18:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AziendaSQL',
            fields=[
                ('id_azienda', models.IntegerField(db_column='Id Azienda', primary_key=True, serialize=False)),
                ('ragione_sociale', models.CharField(db_column='Ragione Sociale', max_length=100)),
                ('descrizione', models.CharField(max_length=200)),
                ('indirizzo', models.CharField(max_length=50)),
                ('citta', models.CharField(max_length=50)),
                ('provincia', models.CharField(max_length=2)),
                ('cap', models.CharField(max_length=5)),
                ('piva', models.CharField(max_length=12)),
                ('cf', models.CharField(max_length=16)),
                ('tel1', models.CharField(max_length=30)),
                ('tel2', models.CharField(max_length=30)),
                ('tel3', models.CharField(max_length=30)),
                ('tel4', models.CharField(max_length=30)),
                ('dtel1', models.CharField(max_length=20)),
                ('dtel2', models.CharField(max_length=20)),
                ('dtel3', models.CharField(max_length=20)),
                ('dtel4', models.CharField(max_length=20)),
                ('sitoweb', models.CharField(max_length=50)),
                ('note', models.CharField(max_length=5000)),
                ('hashragionesociale', models.CharField(max_length=100)),
                ('valido', models.BooleanField()),
                ('accetta_promozioni', models.BooleanField()),
            ],
            options={
                'db_table': 'asc_aziende',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ContattoSQL',
            fields=[
                ('id_contatto', models.IntegerField(db_column='Id Contatto', primary_key=True, serialize=False)),
                ('id_azienda', models.IntegerField(db_column='Id Azienda')),
                ('titolo', models.CharField(max_length=50)),
                ('nome', models.CharField(max_length=50)),
                ('cognome', models.CharField(max_length=50)),
                ('posizione', models.CharField(max_length=50)),
                ('tel1', models.CharField(max_length=30)),
                ('tel2', models.CharField(max_length=30)),
                ('tel3', models.CharField(max_length=30)),
                ('tel4', models.CharField(max_length=30)),
                ('dtel1', models.CharField(max_length=20)),
                ('dtel2', models.CharField(max_length=20)),
                ('dtel3', models.CharField(max_length=20)),
                ('dtel4', models.CharField(max_length=20)),
                ('email1', models.CharField(max_length=20)),
                ('email2', models.CharField(max_length=20)),
                ('data_nascita', models.DateField(db_column='Data Nascita')),
                ('note', models.CharField(max_length=5000)),
            ],
            options={
                'db_table': 'asc_contatti',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='NazioneSQL',
            fields=[
                ('nazione', models.CharField(max_length=80, primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'asc_nazioni',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ProvinciaSQL',
            fields=[
                ('sigla', models.CharField(max_length=2, primary_key=True, serialize=False)),
                ('provincia', models.CharField(max_length=40)),
            ],
            options={
                'db_table': 'asc_provincie',
                'managed': False,
            },
        ),
    ]