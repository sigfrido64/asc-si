# coding=utf-8
from mongoengine import *
from django.db import models
import datetime
from si.si    import concatena, hashsig
# from bson.objectid import ObjectId
"""
    Attenzione che per far funzionare il tutto bisogna creare un indice sparse su CF per evitare l'inserimento di
    valori duplicati nel codice fiscale (Per questo l'indice deve essere di tipo sparse...).
"""


# region Modello MongoDB
class Nazione(Document):
    """
    Collezione delle nazioni note.
    """
    nazione = StringField(max_length=80, required=True, primary_key=True)

    dts_aggiornamento = DateTimeField()
    dts_creazione = DateTimeField()

    def __str__(self):
        return self.nazione

    def save(self, *args, **kwargs):
        if not self.dts_creazione:
            self.dts_creazione = datetime.datetime.now()
        self.dts_aggiornamento = datetime.datetime.now()
        return super(Nazione, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Nazione"
        verbose_name_plural = "Nazioni"
        managed = False


class Provincia(Document):
    """
    Collezione delle Provincie (anche se non esistono più !)
    """
    sigla = StringField(max_length=2, required=True, primary_key=True)
    provincia = StringField(max_length=40)

    dts_aggiornamento = DateTimeField()
    dts_creazione = DateTimeField()

    def __str__(self):
        return concatena(self.provincia, " (", self.sigla, ")")

    def save(self, *args, **kwargs):
        if not self.dts_creazione:
            self.dts_creazione = datetime.datetime.now()
        self.dts_aggiornamento = datetime.datetime.now()
        return super(Provincia, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Provincia"
        verbose_name_plural = "Provincie"
        managed = False


class Azienda(Document):
    """
    Anagrafica Azienda
    """
    ragione_sociale = StringField(max_length=100, required=True)
    descrizione = StringField(max_length=200)
    # Vecchia chiave primaria di Assocam.
    id_asc_azienda = LongField()
    # TODO Devo essere sicuro che non possano essere inseriti due CF Uguali.
    cf = StringField(max_length=16, verbose_name="Codice Fiscale")
    mail_generica = EmailField()
    sito_web = StringField(max_length=50)
    note = StringField()
    hash = StringField(max_length=100)
    lista_sedi_html = StringField(max_length=1000)
    lista_contatti_html = StringField(max_length=2000)
    dts_aggiornamento = DateTimeField()
    dts_creazione = DateTimeField()
    # Definizione degli indici
    # Nello specifico indice testuale su hash.
    meta = {
        'indexes': ['$hash'],
        'collection': 'aziende_aziende'
    }

    def __str__(self):
        return self.ragione_sociale

    def save(self, *args, **kwargs):
        # Compone l'Hash dell'azienda.
        self.hash = hashsig(self.ragione_sociale)

        # Aggiorna i timestamps.
        if not self.dts_creazione:
            self.dts_creazione = datetime.datetime.now()
        self.dts_aggiornamento = datetime.datetime.now()
        return super(Azienda, self).save(*args, **kwargs)

    def aggiornacorrelazioni(self):
        """
        Aggiorna gli elementi delle correlazioni.
        """
        # Compone la lista delle sedi.
        sedi = Sede.objects(azienda=self)
        lista_sedi = ''
        for sede in sedi:
            if lista_sedi:
                lista_sedi += '<br>'
            lista_sedi += sede.indirizzo_verboso
        self.lista_sedi_html = lista_sedi

        # Compone la lista dei contatti.
        contatti = Contatto.objects(azienda=self)
        lista_contatti = ''
        for conta in contatti:
            if lista_contatti:
                lista_contatti += '<br>'
            lista_contatti += conta.contatto_verboso
        self.lista_contatti_html = lista_contatti

        # Infine salva l'istanza.
        self.save()

    class Meta:
        managed = False


class Sede(Document):
    """
    Sede di un'Azienda.
    """
    # _id = ObjectIdField(required=True, default=lambda: ObjectId())
    # Riferimento alla vecchia matricola Assocam
    id_asc_azienda = LongField()
    # Riferimento al record correlato dell'Azienda.
    azienda = ReferenceField(Azienda, reverse_delete_rule=DENY)
    # Campi specifici della singola sede.
    piva = StringField(max_length=12)
    indirizzo1 = StringField(max_length=50)
    indirizzo2 = StringField(max_length=50)
    comune = StringField(max_length=50)
    provincia = StringField(max_length=2)
    cap = StringField(max_length=5)
    nazione = StringField(max_length=50)
    indirizzo_verboso = StringField(max_length=200)
    tel1 = StringField(max_length=30)
    tel2 = StringField(max_length=30)
    tel3 = StringField(max_length=30)
    tel4 = StringField(max_length=30)
    doctel1 = StringField(max_length=20)
    doctel2 = StringField(max_length=20)
    doctel3 = StringField(max_length=20)
    doctel4 = StringField(max_length=20)
    sede_legale = BooleanField(default=False)
    attivo = BooleanField(default=True)
    promozione_ok = BooleanField(default=True)
    note = StringField()
    # contatti = EmbeddedDocumentListField(EmbeddedDocumentField(Contatto))
    dts_aggiornamento = DateTimeField()
    dts_creazione = DateTimeField()
    # Definizione degli indici.
    # Nello specifico su id_asc_azienda in quanto parte delle ricerche saranno fatte qui.
    meta = {
        'indexes': ['id_asc_azienda'],
        'collection': 'aziende_sedi'
    }

    def __str__(self):
        return self.indirizzo_verboso

    def save(self, *args, **kwargs):
        # Compone l'indirizzo verboso dell'azienda.
        dummy = concatena(self.indirizzo1, " ", self.indirizzo2, " - ", self.cap, " ", self.comune, " (",
                          self.provincia, ")")
        if self.nazione:
            dummy = concatena(dummy, " - ", self.nazione)
        self.indirizzo_verboso = dummy

        # Aggiorna i Timestamps.
        if not self.dts_creazione:
            self.dts_creazione = datetime.datetime.now()
        self.dts_aggiornamento = datetime.datetime.now()

        # Chiama il Super !
        return super(Sede, self).save(*args, **kwargs)

    class Meta:
        managed = False


class Contatto(Document):
    """
    Contatto all'interno di un'azienda.
    """
    # _id = ObjectIdField(required=True, default=lambda: ObjectId())
    # Riferimento alla vecchia matricola Assocam
    id_asc_azienda = LongField()
    id_asc_contatto = LongField()
    # Riferimento al record correlato dell'Azienda.
    azienda = ReferenceField(Azienda, reverse_delete_rule=DENY)
    sede = ReferenceField(Sede, reverse_delete_rule=DENY)
    # Campi specifici della singola sede.
    titolo = StringField(max_length=50)
    nome = StringField(max_length=50)
    cognome = StringField(max_length=50)
    posizione = StringField(max_length=50)
    contatto_verboso = StringField(max_length=200)
    tel1 = StringField(max_length=30)
    tel2 = StringField(max_length=30)
    tel3 = StringField(max_length=30)
    tel4 = StringField(max_length=30)
    doctel1 = StringField(max_length=20)
    doctel2 = StringField(max_length=20)
    doctel3 = StringField(max_length=20)
    doctel4 = StringField(max_length=20)
    email1 = EmailField()
    email2 = EmailField()
    data_nascita = DateTimeField()
    note = StringField()
    attivo = BooleanField(default=True)
    promozione_ok = BooleanField(default=True)
    hash = StringField(max_length=100)
    # Timestamp di creazione e di aggiornamento.
    dts_aggiornamento = DateTimeField()
    dts_creazione = DateTimeField()
    # Definizione degli indici.
    # Nello specifico su id_asc_azienda e su id_asc_contatto in quanto parte delle ricerche saranno fatte qui.
    meta = {
        'indexes': ['id_asc_azienda', 'id_asc_contatto'],
        'collection': 'aziende_contatti'
    }

    def __str__(self):
        return concatena(self.titolo, " ", self.cognome, " ", self.nome)

    def save(self, *args, **kwargs):
        # Calcola l'hash del contatto
        self.hash = hashsig(concatena(self.cognome, self.nome))

        # Compone il contatto verboso per il seguito.
        self.contatto_verboso = concatena(self.titolo, ' ', self.cognome, ' ', self.nome)

        # Aggiorna i Timestamps.
        if not self.dts_creazione:
            self.dts_creazione = datetime.datetime.now()
        self.dts_aggiornamento = datetime.datetime.now()

        # Chiama il super !
        return super(Contatto, self).save(*args, **kwargs)

    class Meta:
        managed = False
# endregion


# region API IMPORTAZIONE ASSOCAM
class NazioneSQL(models.Model):
    nazione = models.CharField(max_length=80, primary_key=True)

    class Meta:
        managed = False
        db_table = 'asc_nazioni'


class ProvinciaSQL(models.Model):
    sigla = models.CharField(max_length=2, primary_key=True)
    provincia = models.CharField(max_length=40)

    class Meta:
        managed = False
        db_table = 'asc_provincie'


class AziendaSQL(models.Model):
    id_azienda = models.IntegerField(primary_key=True, db_column='Id Azienda')
    ragione_sociale = models.CharField(max_length=100, db_column="Ragione Sociale")
    descrizione = models.CharField(max_length=200)
    indirizzo = models.CharField(max_length=50)
    citta = models.CharField(max_length=50)
    provincia = models.CharField(max_length=2)
    cap = models.CharField(max_length=5)
    piva = models.CharField(max_length=12)
    cf = models.CharField(max_length=16)
    tel1 = models.CharField(max_length=30)
    tel2 = models.CharField(max_length=30)
    tel3 = models.CharField(max_length=30)
    tel4 = models.CharField(max_length=30)
    dtel1 = models.CharField(max_length=20)
    dtel2 = models.CharField(max_length=20)
    dtel3 = models.CharField(max_length=20)
    dtel4 = models.CharField(max_length=20)
    sitoweb = models.CharField(max_length=50)
    note = models.CharField(max_length=5000)
    hashragionesociale = models.CharField(max_length=100)
    valido = models.BooleanField()
    accetta_promozioni = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'asc_aziende'


class ContattoSQL (models.Model):
    id_contatto = models.IntegerField(primary_key=True, db_column='Id Contatto')
    id_azienda = models.IntegerField(db_column='Id Azienda')
    titolo = models.CharField(max_length=50)
    nome = models.CharField(max_length=50)
    cognome = models.CharField(max_length=50)
    posizione = models.CharField(max_length=50)
    tel1 = models.CharField(max_length=30)
    tel2 = models.CharField(max_length=30)
    tel3 = models.CharField(max_length=30)
    tel4 = models.CharField(max_length=30)
    dtel1 = models.CharField(max_length=20)
    dtel2 = models.CharField(max_length=20)
    dtel3 = models.CharField(max_length=20)
    dtel4 = models.CharField(max_length=20)
    email1 = models.CharField(max_length=20)
    email2 = models.CharField(max_length=20)
    data_nascita = models.DateField(db_column='Data Nascita')
    note = models.CharField(max_length=5000)

    class Meta:
        managed = False
        db_table = 'asc_contatti'

# endregion
