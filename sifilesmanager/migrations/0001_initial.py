# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sifilesmanager.models
import django.core.files.storage
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='INode',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('nome', models.CharField(max_length=80)),
                ('descrizione', models.TextField(max_length=200)),
                ('data_aggiornamento', models.DateTimeField(auto_now=True)),
                ('data_creazione', models.DateTimeField(auto_now_add=True)),
                ('padre', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, default=None, blank=True, null=True, to='sifilesmanager.INode')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SiFile',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('nome', models.CharField(max_length=80)),
                ('descrizione', models.TextField(max_length=200)),
                ('sha1_hash', models.CharField(unique=True, max_length=40, db_index=True)),
                ('pathurl', models.CharField(max_length=2)),
                ('url', models.CharField(max_length=38)),
                ('filename', models.FileField(upload_to=sifilesmanager.models.upload_to_sha1, storage=django.core.files.storage.FileSystemStorage(location='D:\\Seafile\\Py\\si\\data'))),
                ('size', models.PositiveIntegerField(default=0)),
                ('data_aggiornamento', models.DateTimeField(auto_now=True)),
                ('data_creazione', models.DateTimeField(auto_now_add=True)),
                ('inode', models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, null=True, to='sifilesmanager.INode')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
