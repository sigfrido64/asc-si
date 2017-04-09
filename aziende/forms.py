# coding=utf-8
from django.forms import TextInput
from .models import Nazione, Azienda
from mongodbforms import DocumentForm


class NazioneForm(DocumentForm):

    class Meta:
        model = Nazione

        fields = ['nazione']

        widgets = {
            'nazione': TextInput(attrs={'class': 'easyui-textbox', 'style': 'width:300px'}),
        }


class AziendaForm(DocumentForm):

    class Meta:
        model = Azienda
