# coding=utf-8
from .models import Corso
from mongodbforms import DocumentForm, CharField
from sigwidgets import JqxDateTimeInput, JqxInput, JqxTextArea, JqxComboBox, JqxDataGrid


class CorsoForm(DocumentForm):
    lezioni = CharField(widget=JqxDataGrid(
        jqwattrs={'width': '100%', 'url': '/si/corsi/api/get_corsi/',
                  'columns': [
                    {'text': 'Codice Corso', 'dataField': 'codice', 'width': '10%'},
                    {'text': 'Denominazione', 'dataField': 'denominazione', 'width': '70%'},
                    {'text': 'Durata', 'dataField': 'durata', 'width': '10%'},
                    {'text': 'Ordine', 'dataField': 'ordine', 'width': '10%'}
                    ],
                  }))
"""
    class Meta:
        model = Corso
        fields = ['codice_edizione', 'denominazione', 'durata', 'partecipanti',
                  'docente', 'note', 'stato']
        # attrs="{height: 25, w-+idth: 400, minLength: 5}"
        widgets = {
            'codice_edizione': JqxInput(jqwattrs={'width': 100, 'minLength': 5}),
            'denominazione': JqxInput(jqwattrs={'width': 400, 'minLength': 5}),
            'durata': JqxInput(jqwattrs={'width': 50, 'minLength': 5}),
            'partecipanti': JqxInput(jqwattrs={'width': 50, 'minLength': 5}),
            'docente': JqxInput(jqwattrs={'width': 400, 'minLength': 5}),
            'note': JqxTextArea(jqwattrs={'height': 90, 'width': 300}),
            'stato': JqxComboBox(jqwattrs={'height': 25, 'width': 100, 'source': ['BOZZA', 'PIANIFICATO']})
        }

"""