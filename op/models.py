# coding=utf-8

from mongoengine import *


class OrdineProduzione(Document):
    """
    Definisce l'ordine di produzione per i corsi.
    """
    ordine_numero = StringField(max_length=10, required=True, primary_key=True)
    # Interno o esterno hanno ancora un senso ?

    committenti = StringField(max_length=100)
    corsi = StringField(max_length=200)
    persona_di_riferimento = StringField()

    cup = StringField(max_length=20)
    cig = StringField(max_length=20)

    stato = StringField(max_length=20)
    cdc = StringField(max_length=10, verbose_name='Centro di Costo')

    data_inizio = DateTimeField()
    data_fine = DateTimeField()

    prot_gestione = IntField()

    note = StringField(max_length=200)

    dts_aggiornamento = DateTimeField()
    dts_creazione = DateTimeField()

    def __str__(self):
        return self.ordine_numero

"""
You could override the save method.
Gestione delle date di aggiornamento e creazione di un record !

class MyModel(mongoengine.Document):
    creation_date = mongo.DateTimeField()
    modified_date = mongo.DateTimeField(default=datetime.datetime.now)

    def save(self, *args, **kwargs):
        if not self.creation_date:
            self.creation_date = datetime.datetime.now()
        self.modified_date = datetime.datetime.now()
        return super(MyModel, self).save(*args, **kwargs)



shareimprove this answer
answered Nov 15 '11 at 21:34

Willian
1,484713

This is exactly what I needed. I had figured out the default bit, but overriding the save method to track the modified time is perfect. Thank you :) –  Dawson Feb 4 '14 at 18:21

The problem with this though is that the save function won't be called if you do an update instead of a .save right? –  Brenden1995 Jul 10 at 2:16

@Brenden1995 Nope, it doesn't work with update. –  Willian Jul 13 at 11:36
"""

"""
    diario = ListField(EmbeddedDocumentField(Log))

"""

"""
class Committente(EmbeddedDocument):
    Definisce un'azienda o un ente che commissiona il corso

    azienda = StringField(max_length=120)
    azienda_pk = IntField()
    riferimento_tecnico = StringField(max_length=120)
    riferimento_tecnico_pk = IntField()
    riferimento_amministrativo = StringField(max_length=120)
    riferimento_amministrativo_pk = IntField()

    def __str__(self):
        return self.azienda


class Log(EmbeddedDocument):
    Registrazione di un contatto con il cliente.
    autore = StringField()
    contenuto = MultiLineStringField()
    dts = DateTimeField()


"""