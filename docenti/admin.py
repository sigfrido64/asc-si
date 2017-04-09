# coding=utf-8
from django.contrib import admin

# Register your models here.
from docenti.models import Docente, IncaricoDocenza

admin.site.register(Docente)


class IncaricoDocenzaAdmin(admin.ModelAdmin):
    """
        Definizione dell'interfaccia amministrativa dell'incarico di docenza.
    """
    fields = ('proposta_numero', 'data_proposta',
              ('data_inizio', 'data_fine'),
              'codice_corso', 'docente',
              'descrizione', 'ore_previste',
              'parametro',
              'extra_compenso', 'extra_compenso_motivazione',
              'compenso_totale_previsto',
              'tipologia_fornitore',
              'iniziativa', 'gruppo', 'gruppo_sub1',
              'data_aggiornamento')

    readonly_fields = ('data_aggiornamento',)


admin.site.register(IncaricoDocenza, IncaricoDocenzaAdmin)
