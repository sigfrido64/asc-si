# coding=utf-8
from django.forms import Textarea, TextInput
from .models import OrdineProduzione
from mongodbforms import DocumentForm


class OrdineProduzioneForm(DocumentForm):

    class Meta:
        model = OrdineProduzione

        fields = ['ordine_numero', 'committenti', 'persona_di_riferimento', 'corsi', 'stato', 'cup', 'cig', 'cdc',
                  'prot_gestione', 'note']

        widgets = {
            'ordine_numero': TextInput(attrs={'class': 'easyui-textbox'}),
            'committenti': TextInput(attrs={'class': 'easyui-textbox', 'style': 'width:300px'}),
            'cup': TextInput(attrs={'class': 'easyui-textbox'}),
            'persona_di_riferimento': TextInput(attrs={'class': 'easyui-textbox'}),
            'cig': TextInput(attrs={'class': 'easyui-textbox'}),
            'stato': TextInput(attrs={'class': 'easyui-textbox'}),
            'cdc': TextInput(attrs={'class': 'easyui-textbox'}),
            'prot_gestione': TextInput(attrs={'class': 'easyui-textbox'}),
            'corsi': TextInput(attrs={'class': 'easyui-textbox', 'style': 'width:300px'}),
            'note': Textarea(attrs={'class': 'easyui-textbox', 'data-options': 'multiline:true',
                                    'style': 'width:300px;height:100px'}),
        }


"""

class CommittenteForm(EmbeddedDocumentForm):
    class Meta:
        document = Committente
        embedded_field_name = 'committenza'

        fields = ['azienda']

'data_fine': DateInput(attrs={'class': 'easyui-datebox'}),

    # data1 = forms.DateField(label='Data Inizio', widget=DateInput(attrs={'class': 'easyui-datebox'}))
    # sega = forms.CharField(label='Committeza Sig', widget=TextInput(attrs={'class': 'easyui-textbox'}))


"""
