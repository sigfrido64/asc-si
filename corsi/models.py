# coding=utf-8
"""
    Corsi
"""
from mongoengine import *
from tasker.models import Task
from si.sigutil import concatena
import datetime


class CartelleCorsoTask(Task):
    # Lista dei possibili stati
    STATO_ESEGUITO = 100
    STATO_IN_LAVORAZIONE = 10
    STATO_ATTESA_LAVORAZIONE = 0
    STATO_ERRORE = -1
    STATO_ATTESA_GESTIONE_ERRORE = -2
    STATO_ARCHIVIARE = -10
    # Nome del processo distribuito per gli heartbeat
    PROCESSO = "Cartelle Corso"
    # Timeout prima di considerare il processo morto
    TIMEOUT = 360
    # Tempo per il quale il task deve dormire tra un'iterazione e l'altra.
    # LOOP < TIMEOUT ovviamente !!!
    LOOP = 300

    # Finalmente definisco i campi !
    corso = StringField()
    anno_formativo = StringField()
    tipologia = StringField()


class Lezione(EmbeddedDocument):
    """
    Definizione di una lezione.
    """
    id = ObjectIdField(primary_key=True, required=True)
    data = StringField()
    inizio = StringField()
    fine = StringField()
    sede = StringField()
    # Campi compilati al salvataggio
    data_annodoy = IntField()
    orainizio = IntField()
    orafine = IntField()


class Corso(Document):
    """
    Definizione del corso
    """
    codice_edizione = StringField(primary_key=True, max_length=10)
    denominazione = StringField(max_length=150)
    ordine = ReferenceField('OrdineProduzione')
    durata = IntField(default=8, min_value=1)
    note = StringField(max_length=1000)
    partecipanti = IntField(default=16, min_value=1)
    docente = StringField()
    cartella_corso = BooleanField(default=False)
    stato = StringField(default='BOZZA')
    stato_si = IntField(min_value=0, default=CartelleCorsoTask.STATO_ATTESA_LAVORAZIONE)
    # Lezioni del corso.
    lezioni = EmbeddedDocumentListField(Lezione)

    # Campi compilati durante il salvataggio.
    data_inizio = StringField()
    data_inizio_annodoy = IntField(default=0)
    data_fine = StringField()
    data_fine_annodoy = IntField(default=0)
    # Timestamp di creazione e di aggiornamento.
    dts_aggiornamento = DateTimeField()
    dts_creazione = DateTimeField()
    # Definizione degli indici
    meta = {
        'indexes': ['lezioni.doy', 'lezioni.id']
    }

    def __str__(self):
        return concatena(self.codice_edizione, ' ', self.denominazione)

    def save(self, *args, **kwargs):
        # Aggiorna i Timestamps.
        if not self.dts_creazione:
            self.dts_creazione = datetime.datetime.now()
        self.dts_aggiornamento = datetime.datetime.now()

        # Chiama il super !
        return super(Corso, self).save(*args, **kwargs)

    class Meta:
        managed = False
        verbose_name = "Corso"
        verbose_name_plural = "Corsi"


"""
    def clean(self):
        print("Inizio la validazione")
        
        # La durata del corso deve essere di almeno un'ora.

        if self.durata < 2:
            raise ValidationError(field_name='Adurata', message="Must be louder!")
            #message='La durata del corso deve essere positiva.')
        self.errors = kwargs.get('errors', {})
        self.field_name = kwargs.get('field_name')
        self.message = message


        # La data di inizio deve essere maggiore o uguale a quella di fine.
        #if self.data_fine < self.data_inizio:
        #    raise ValidationError({'data_fine': 'La data di fine corso deve essere maggiore o uguale a quella '
        #                                        'di inizio corso.'})
        self.codice_edizione = self.codice_edizione.upper()
    """

"""
class CorsoA(models.Model):
    Definizione dei corsi
    BOZZA = 0
    PIANIFICATO = 10

    STATO_CORSO_CHOICES = (
        (BOZZA, u'Bozza'),
        (PIANIFICATO, u'Pianificato'),
    )

    codice_edizione = models.CharField(primary_key=True, max_length=10, validators=[MinLengthValidator(6)])
    denominazione = models.CharField(max_length=150, validators=[MinLengthValidator(10)])
    data_inizio = models.DateField()
    data_fine = models.DateField()
    durata = models.IntegerField(default=8)
    stato = models.IntegerField(choices=STATO_CORSO_CHOICES, default=BOZZA)
    raggruppamento = models.ForeignKey('iniziative.Raggruppamento')
    # modello = models.ForeignKey(Modello)
    note = models.CharField(max_length=1000)

    data_aggiornamento = models.DateTimeField(auto_now=True)
    data_creazione = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Corso"
        verbose_name_plural = "Corsi"

    def __str__(self):
        return self.codice_edizione + ' ' + self.denominazione

    def clean(self):
            Validazione del modello nel suo complesso.
        # La durata del corso deve essere di almeno un'ora.
        if self.durata <= 0:
            raise ValidationError({'durata': 'La durata del corso deve essere positiva.'})

        # La data di inizio deve essere maggiore o uguale a quella di fine.
        if self.data_fine < self.data_inizio:
            raise ValidationError({'data_fine': 'La data di fine corso deve essere maggiore o uguale a quella '
                                                'di inizio corso.'})
        self.codice_edizione = self.codice_edizione.upper()


class TimeSlot(models.Model):
    Definizione del Time Slot
    NORMALE = 0
    RECUPERO = 0

    TIPOLOGIA_CHOICES = (
        (NORMALE, u'Normale'),
        (RECUPERO, u'Recupero'),
    )

    corso = models.ForeignKey(Corso)
    inizio = models.DateTimeField()
    fine = models.DateTimeField()
    durata = models.FloatField()
    anno = models.IntegerField()
    doy = models.IntegerField()
    tipologia = models.IntegerField(choices=TIPOLOGIA_CHOICES, default=NORMALE)

    data_aggiornamento = models.DateTimeField(auto_now=True)
    data_creazione = models.DateTimeField(auto_now_add=True)

    # Imposta i campi calcolati prima di salvare
    def save(self, *args, **kwargs):
        # Salva il nome del file in nome.
        self.durata = self.fine - self.inizio
        self.anno = 100

        super(TimeSlot, self).save(*args, **kwargs)

"""