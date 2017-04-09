# coding=utf-8
"""
 Ulcuni siti interessanti quanto a gestione del Fors.
 http://www.onespacemedia.com/news/2014/feb/5/getting-started-generic-class-based-views-django/
 http://tumivn.com/2014/09/16/develop-a-crud-movie-app-with-django-1-7/

 ORDINE GENEALE DELLE VISTE

 Index
 Add
 Edit
 Delete
 Detail


    poll = Poll.objects(question__contains="What").first()
    choice = Choice(choice_text="I'm at DjangoCon.fi", votes=23)
    poll.choices()
    poll.save()

    segnalazione = Segnalazione(corso='APQI',
                                corso_descrizione='Addetto Prevenzione Incendi',
                                azienda='Canistracci S.p.a.',
                                azienda_pk=10,
                                contatto='Mr. Pillow',
                                contatto_pk=11,
                                persone=2,
                                valida=True
                                )
    segnalazione.save()

    print(segnalazione)

    corso = StringField(max_length=10)
    corso_descrizione = StringField(max_length=80)

    azienda = StringField(max_length=120)
    azienda_pk = IntField()

    contatto = StringField(max_length=120)
    contatto_pk = IntField()

    persone = IntField(default=1)

    data_ricezione = DateTimeField(help_text='Data ricezione segnalazione di interesse')
    data_aggiornamento = DateTimeField()
    data_creazione = DateTimeField()


    poll = Poll.objects(question__contains="merda").first()
    choice = Choice(choice_text="Pippo e pluto", votes=23)
    poll.choices.append(choice)
    poll.save()
    print(poll)

    return HttpResponse(request, "Fatto")



"""
# from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.urlresolvers import reverse
from .forms import CorsoBaseForm
from django.shortcuts import render
from .models import CorsiPerSegnalazioni, Segnalazione, Persone


"""from django.contrib.auth.decorators import login_required

from django.core.urlresolvers import reverse
from .forms import SottoIniziativaForm, GruppoForm
from django.views.generic import CreateView, UpdateView
import json
"""


@login_required()
def sega(request):
    """
    Usata per inserimenti di prova.
    TODO : Da eliminare quando tutto ok !!!
    """
    corso = CorsiPerSegnalazioni.objects.get(codice_base='A08I')

    persona1 = Persone(pax=2, stato=2)
    persona2 = Persone(pax=1, stato=0)

    segnalazione = Segnalazione(corso=corso, azienda='canistracci', contatto='me medesimo')
    segnalazione.persone = [persona1, persona2]
    segnalazione.save()

    # Visualizza la risposta.
    return HttpResponse("Fatto !!")


@login_required()
def index_a(request, pk):
    """
    SEGNALAZIONI : Indice generale dei codici corso di base ordinato per codice corso.
    """
    corso = CorsiPerSegnalazioni.objects.get(codice_base=pk)

    lista_segnalazioni = Segnalazione.objects(corso=corso)
    context_dict = {'lista_segnalazioni': lista_segnalazioni, 'corso': corso}

    # Visualizza la risposta.
    return render(request, 'segnalazioni/index_a.html', context_dict)


@login_required()
def index(request):
    """
    SEGNALAZIONI : Indice generale dei codici corso di base ordinato per codice corso.
    """
    lista_corsibase = CorsiPerSegnalazioni.objects().order_by('codice_base')
    context_dict = {'lista_corsibase': lista_corsibase}

    # Visualizza la risposta.
    return render(request, 'segnalazioni/index.html', context_dict)


@login_required()
def corsobase_cu(request, pk=None):
    """
    CORSO BASE : Modifica dei dati del codice corso di base e creazione di un nuovo codice.
    """
    # Cerca di recuperare i dati del corso di base e se non ci riesce segnala errore.
    # TODO servirebbe la funzione standard get_object_or_404 per ridurre tutto ad una linea.
    if pk:
        try:
            corsobase = CorsiPerSegnalazioni.objects.get(codice_base=pk)
        except CorsiPerSegnalazioni.DoesNotExist:
            raise Http404('Il corso richiesto non esiste !')
    else:
        corsobase = CorsiPerSegnalazioni()
        corsobase.dts_creazione = timezone.now()

    # Legge i dati dal POST e li analizza per salvarli.
    if request.method == 'POST':
        corsobase.dts_aggiornamento = timezone.now()
        form = CorsoBaseForm(request.POST, instance=corsobase)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('segnalazioni:index'))
    else:
        form = CorsoBaseForm(instance=corsobase)

    # Popola il dizionario per il template e lo visualizza.
    context_dict = {'form': form, 'blocktitle': 'Corso Base', 'header':
                    'Corso base per segnalazione (creato : ' + str(corsobase.dts_creazione) + ' ultimo agg : ' +
                    str(corsobase.dts_aggiornamento) + ')'}
    return render(request, 'si_cu_formasp_t1.html', context_dict)


@login_required()
def corsobase_del(request, pk):
    """
    GRUPPO : Elimina il raggruppamento.

    Non chiede conferma perchè la richiesta viene fatta a monte, prima di chiamare questa funzione.
    """
    # Cerca di recuperare l'elemento e se non ci riesce segnala errore.
    try:
        corsobase = CorsiPerSegnalazioni.objects.get(codice_base=pk)
    except CorsiPerSegnalazioni.DoesNotExist:
        raise Http404('Il corso richiesto non esiste !')

    # Procede con la cancellazione e torna alla lista dei corsi per segnalazioni.
    corsobase.delete()
    return HttpResponseRedirect(reverse('segnalazioni:index'))
