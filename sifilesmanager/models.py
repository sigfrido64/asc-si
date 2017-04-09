# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import hashlib
import os


fs = FileSystemStorage(location=settings.SIFILEDATA_ROOT)


def upload_to_sha1(instance, filename):
    full_path = os.path.normcase(os.path.normpath(instance.pathurl))
    dest = os.path.join(full_path, instance.url)
    print(dest)
    return dest


class INode(models.Model):
    """
    I Node.
    Sono i nomi delle Cartelle in cui organizzo i files.
    """
    nome = models.CharField(max_length=80)
    descrizione = models.TextField(max_length=200)
    padre = models.ForeignKey('self', on_delete=models.PROTECT, null=True, blank=True, default=None)
    data_aggiornamento = models.DateTimeField(auto_now=True)
    data_creazione = models.DateTimeField(auto_now_add=True)


class SiFile(models.Model):
    """
    Modello dei files memorizzati con chiave sha1 per memorizzazione efficiente.
    """
    nome = models.CharField(max_length=80)
    descrizione = models.TextField(max_length=200)
    sha1_hash = models.CharField(db_index=True, max_length=40, unique=True)  # TODO non deve essere NULL
    pathurl = models.CharField(max_length=2)
    url = models.CharField(max_length=38)
    filename = models.FileField(upload_to=upload_to_sha1, storage=fs)  # TODO che faccio con le collisioni ?
    inode = models.ForeignKey(INode, on_delete=models.PROTECT, null=True, blank=False, default=None)
    size = models.PositiveIntegerField(default=0)
    data_aggiornamento = models.DateTimeField(auto_now=True)
    data_creazione = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Salva il nome del file in nome.
        self.nome = self.filename
        self.size = self.filename.size

        # Salva l'hash sha1 del file in sha1_hash
        h = hashlib.sha1()
        for chunk in self.filename.chunks():
            h.update(chunk)
        sha1 = h.hexdigest()
        self.sha1_hash = sha1

        # Compone i campi di urlpath e di url per la memorizzazione del file.
        self.url = sha1[2:]
        self.pathurl = sha1[:2]

        super(SiFile, self).save(*args, **kwargs)