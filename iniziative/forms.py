# coding=utf-8
from django.forms import ModelForm, Textarea, TextInput, CharField, Form
from .models import Iniziativa, SottoIniziativa, Raggruppamento
from sigwidgets import JqxInput, JqxDataGrid
__author__ = 'Sig'


class ListaIniziativeForm(Form):
    """
    Form per la lista delle iniziative
    """
    your_name = CharField(widget=JqxDataGrid(jqwattrs={
            'width': '100%', 'url': '/si/iniziative/api/get_iniziative/',
            'columns': [
                {'text': 'Nome', 'dataField': 'nome', 'width': '20%'},
                {'text': 'Descrizione', 'dataField': 'descrizione', 'width': '80%'}
            ],
        }))


class IniziativaForm(ModelForm):
    """
    Form per l'aggiunta/modifica delle iniziative.
    """
    class Meta:
        model = Iniziativa
        fields = ['nome', 'descrizione']
        widgets = {
            'nome': JqxInput(jqwattrs={'width': 100, 'minLength': 5}),
            'descrizione': JqxInput(jqwattrs={'width': 400, 'minLength': 5})
        }
    

class SottoIniziativaForm(ModelForm):
    """
    Attenzione che il campo iniziativa che è una chiave esterna non lo metto proprio così il form potrà essere
    validato senza errori.
    Dopo la validazione scrivo la chiave esterna e poi lo salvo ma tutto questo lo farò nella view !
    """
    class Meta:
        model = SottoIniziativa
        fields = ['nome', 'descrizione', 'in_uso']
        widgets = {
            'nome': TextInput(attrs={'size': 60}),
            'descrizione': Textarea(attrs={'cols': 40, 'rows': 2}),
        }


class GruppoForm(ModelForm):
    """
    Attenzione che il campo sotto-iniziativa che è una chiave esterna non lo metto proprio così il form potrà essere
    validato senza errori.
    Dopo la validazione scrivo la chiave esterna e poi lo salvo ma tutto questo lo farò nella view !
    """
    class Meta:
        model = Raggruppamento
        fields = ['nome', 'descrizione', 'ordine', 'in_uso']
        widgets = {
            'nome': TextInput(attrs={'size': 60}),
            'descrizione': Textarea(attrs={'cols': 40, 'rows': 2}),
            'ordine': TextInput(attrs={'size': 60}),
        }
