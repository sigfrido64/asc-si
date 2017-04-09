# coding=utf-8
from import_export import resources
from .models import TabellaStatoOrdini


class OrdacqResource(resources.ModelResource):
    class Meta:
        model = TabellaStatoOrdini
        exclude = ('data_aggiornamento', 'data_creazione')
