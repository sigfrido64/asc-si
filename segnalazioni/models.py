# coding=utf-8
# from django.db import models
from mongoengine import *


class Persone(EmbeddedDocument):
    """
    Registro le possibili prenotazioni che mi fa l'azienda.
    """
    pax = IntField(default=1)
    stato = IntField(default=0)

    def __str__(self):
        return str(self.pax) + ' - ' + " stato : " + str(self.stato)


class Log(EmbeddedDocument):
    """
    Registrazione di un contatto con il cliente.
    """
    autore = StringField()
    contenuto = MultiLineStringField()
    dts = DateTimeField()


class CorsiPerSegnalazioni(Document):
    """
    Definizione del corso per le segnalazioni di interesse.
    """
    codice_base = StringField(max_length=10, required=True, unique=True)
    denominazione = StringField(max_length=80, required=True)

    tipo = IntField(default=0)
    subtipo = IntField(default=0)

    valido = BooleanField(default=True)

    dts_aggiornamento = DateTimeField()
    dts_creazione = DateTimeField()

    meta = {
        'indexes': [
            'codice_base',
        ]
    }

    def __str__(self):
        return self.codice_base + ' - ' + self.denominazione


class Segnalazione(Document):
    """
    Definizione di una segnalazione di interesse.
    """
    corso = ReferenceField(CorsiPerSegnalazioni, reverse_delete_rule=DENY)
    """
    corso = StringField(max_length=10)
    corso_descrizione = StringField(max_length=80)
    """
    azienda = StringField(max_length=120)
    azienda_pk = IntField()

    contatto = StringField(max_length=120)
    contatto_pk = IntField()

    valido = BooleanField(default=True)

    persone = ListField(EmbeddedDocumentField(Persone))
    logs = ListField(EmbeddedDocumentField(Log))

    data_ricezione = DateTimeField(help_text='Data ricezione segnalazione di interesse')
    data_aggiornamento = DateTimeField()
    data_creazione = DateTimeField()


