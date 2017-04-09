# coding=utf-8
#from django.conf.app_template import models
from django.db import models

# Create your models here.


class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')


class Documento(models.Model):
    nome = models.CharField(max_length=128)     # Nome del file
    sha1 = models.CharField(max_length=128)     # Firma SHA1
    stato = models.PositiveIntegerField(default=0)         # Stato per gestione delle firme

    def __str__(self):
        return self.nome


class Firmatario(models.Model):
    documento = models.ForeignKey(Documento)    # Riferimento al documento da firmare
    utente = models.IntegerField                # TODO : Riferimento all'utente che deve firmare.
    firma = models.DateTimeField                # Data ed ora delle firma, se apposta
    note = models.CharField(max_length=256)     # Note se non ha firmato sul perchè

    def __str__(self):
        return self.utente


class Messaggio(models.Model):
    documento = models.ForeignKey(Documento)    # Riferimento al documento da firmare
    mittente = models.IntegerField                # TODO : Riferimento all'utente che deve firmare.
    destinatario = models.IntegerField                # TODO : Riferimento all'utente che deve firmare.
    testo = models.CharField(max_length=256)    # Testo del messaggio
    letto = models.BooleanField(default=False)  # True se il messaggio è stato letto