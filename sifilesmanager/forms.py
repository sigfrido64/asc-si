# -*- coding: utf-8 -*-
__author__ = 'Sig'
from django.forms import ModelForm
from .models import SiFile, INode


class SiFileForm(ModelForm):
    """
    Qui mostro sono il nome e la descrizione per la finestra di popup.
    """
    class Meta:
        model = SiFile
        fields = ['filename', 'descrizione']


class INodeForm(ModelForm):
    """
    Attenzione che il campo 'padre' che è una chiave esterna non lo metto proprio così il form potrà essere
    validato senza errori.
    Dopo la validazione scrivo la chiave esterna e poi lo salvo ma tutto questo lo farò nella view !
    """
    class Meta:
        model = INode
        fields = ['nome', 'descrizione']
