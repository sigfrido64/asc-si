# -*- coding: utf-8 -*-
"""
    Task di sistema.
"""
from mongoengine import fields, Document
import datetime
from django.db import models
from django.contrib.auth.models import User


class CartelleCorso(Document):
    """
    A seconda della tipologia indicata indico quali cartelle corso sono da copiare.
    """
    tipologia = fields.StringField(primary_key=True)
    cartelle = fields.ListField(fields.StringField())


class Task(Document):
    """
    Definizione di un Task.
    """
    in_uso = fields.BooleanField(default=False)
    agente = fields.StringField()

    stato = fields.IntField(default=0)
    data_aggiornamento = fields.DateTimeField(default=datetime.datetime.now)
    data_creazione = fields.DateTimeField(default=datetime.datetime.now)

    # Permette la creazione di sottoclassi da questo modello.
    meta = {'allow_inheritance': True}

    def save(self, *args, **kwargs):
        """if not self.data_creazione:
            self.data_creazione = datetime.datetime.now()
        """
        self.data_aggiornamento = datetime.datetime.now()
        return super(Task, self).save(*args, **kwargs)


class Heartbeats(Document):
    """
    HeartBeat dei vari processi distribuiti.
    """
    processo = fields.StringField(primary_key=True)
    timeout = fields.IntField(default=60)
    data_aggiornamento = fields.DateTimeField(default=datetime.datetime.now)



