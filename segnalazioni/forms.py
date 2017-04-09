# coding=utf-8
__author__ = 'Sig'

# from django.forms import ModelForm
from mongodbforms import DocumentForm
from .models import CorsiPerSegnalazioni, Segnalazione


class CorsoBaseForm(DocumentForm):
    """
    Form per la gestione del corso base.
    """
    class Meta:
        model = CorsiPerSegnalazioni
        fields = ['codice_base', 'denominazione', 'tipo', 'subtipo', 'valido']


class SegnalazioneForm(DocumentForm):
    """
    Form per la gestione delle segnalazioni di interesse.
    """
    class Meta:
        model = Segnalazione
        embedded_field_name = ['persone', 'logs']
        fields = ['corso', 'azienda', 'contatto', 'valido']

