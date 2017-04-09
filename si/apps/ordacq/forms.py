# coding=utf-8
from django import forms
from .models import TabellaStatoOrdini


class TabellaStatoOrdiniForm(forms.ModelForm):
    class Meta:
        model = TabellaStatoOrdini
        fields = ('protocollo', 'contratto', 'data', 'competenza', 'stato', 'fornitore', 'tipo', 'descrizione',
                  'iniziativa', 'imponibile', 'iva_presente', 'iva_detraibile', 'pagamento',
                  'fatture_protocolli', 'note', 'in_uso')
