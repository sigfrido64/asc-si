# coding=utf-8
"""
    Gestione dei docenti
"""
from django.db import models
from django.core.validators import MinLengthValidator


class Docente(models.Model):
    """
    Definizione dei dati anagrafici dei docenti
    """
    in_essere = models.BooleanField(default=False)
    cognome = models.CharField(max_length=50, validators=[MinLengthValidator(2)])
    nome = models.CharField(max_length=100, validators=[MinLengthValidator(3)])
    codice_fiscale = models.CharField(max_length=16)
    parametro = models.FloatField()
    tipologia_fornitore = models.CharField(max_length=10)
    data_aggiornamento = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.cognome + ' ' + self.nome


class IncaricoDocenza(models.Model):
    """
    Definizione di un incarico di docenza.
    Le ATV le mettiamo in un modello a parte.
    """
    proposta_numero = models.CharField(max_length=5)   # Vedere come gestire i buchi e le lettere
    docente = models.ForeignKey(Docente)
    data_proposta = models.DateField(auto_created=True)
    data_inizio = models.DateField(auto_created=True)
    data_fine = models.DateField()
    codice_corso = models.ForeignKey("corsi.Corso")
    descrizione = models.TextField(max_length=200, verbose_name='Descrizione Incarico')
    ore_previste = models.IntegerField()
    parametro = models.FloatField()
    extra_compenso = models.FloatField(default=0, blank=True)
    extra_compenso_motivazione = models.CharField(max_length=200, default='', blank=True)
    compenso_totale_previsto = models.FloatField()
    tipologia_fornitore = models.CharField(max_length=10)
    iniziativa = models.CharField(max_length=20)
    gruppo = models.CharField(max_length=20)
    gruppo_sub1 = models.CharField(max_length=20)

    data_aggiornamento = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Docenza su '   # TODO devo prendere il valore dal campo del record correlato !

