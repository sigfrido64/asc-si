# coding=utf-8
from django.db import models


class Documento(models.Model):
    nome = models.CharField(max_length=128)     # Nome del file
    sha1 = models.CharField(max_length=128)     # Firma SHA1
    stato = models.PositiveIntegerField(default=0)         # Stato per gestione delle firme

    def __str__(self):
        return self.nome


class Ordine(models.Model):
    """
    Ordini !
    """
    anno_formativo = models.CharField(max_length=10)
    fornitore = models.PositiveIntegerField(default=0)
    collaudo_funzionale = models.BooleanField(default=False)
    data_ordine = models.DateTimeField()
    data_consegna = models.DateTimeField()
    destinazione = models.CharField(max_length=50)
    tipologia_materiale = models.PositiveSmallIntegerField()
    tipologia_iva = models.PositiveSmallIntegerField()
    valore_iva = models.DecimalField(max_digits=3, decimal_places=3)
    note = models.CharField(max_length=500)
    valore_Ordine = models.DecimalField(max_digits=3, decimal_places=3)
    ordine_completo = models.BooleanField(default=False)


