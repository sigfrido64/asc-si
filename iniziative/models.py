# -*- coding: utf-8 -*-
from django.db import models
from django.core.validators import MinLengthValidator


class Iniziativa(models.Model):
    """
    Definizione delle iniziative
    """
    nome = models.CharField(
        db_index=True, max_length=80, unique=True, validators=[MinLengthValidator(3)],
        verbose_name="Nome dell'iniziativa")
    descrizione = models.CharField(
        max_length=80, validators=[MinLengthValidator(5)], verbose_name="Breve descrizione dell'iniziativa")
    cup_cig = models.CharField(max_length=80, blank=True, verbose_name='CIG/CUP se presente')
    iva_scaricabile = models.BooleanField(
        db_index=True, default=True, verbose_name="L'IVA delle spese connesse all'iniziativa è scaricabile ?")
    in_uso = models.BooleanField(db_index=True, default=True, verbose_name="L'iniziativa è tutt'ora in uso ?")

    # Date di creazione e di aggiornamento dell'elemento.
    data_aggiornamento = models.DateTimeField(auto_now=True)
    data_creazione = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome + ' - ' + self.descrizione

    class Meta:
        verbose_name = "Iniziativa"
        verbose_name_plural = "Iniziative"


class SottoIniziativa(models.Model):
    """
    Definizione delle sotto-iniziative
    """
    nome = models.CharField(db_index=True, max_length=80)
    descrizione = models.CharField(max_length=80)
    iniziativa = models.ForeignKey(Iniziativa, on_delete=models.PROTECT)
    in_uso = models.BooleanField(db_index=True, default=True)
    
    data_aggiornamento = models.DateTimeField(auto_now=True)
    data_creazione = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome + ' ' + self.descrizione

    class Meta:
        verbose_name = "Sotto Iniziativa"
        verbose_name_plural = "Sotto Iniziative"


class Raggruppamento(models.Model):
    """
    Definizione dei vari raggruppamenti dei corsi
    """
    nome = models.CharField(db_index=True, max_length=80)
    descrizione = models.CharField(max_length=80)
    sotto_iniziativa = models.ForeignKey(SottoIniziativa, on_delete=models.PROTECT)
    in_uso = models.BooleanField(db_index=True, default=True)
    ordine = models.CharField(max_length=10)
    
    data_aggiornamento = models.DateTimeField(auto_now=True)
    data_creazione = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Raggruppamento"
        verbose_name_plural = "Raggruppamenti"

    def __str__(self):
        return self.nome + ' ' + self.descrizione