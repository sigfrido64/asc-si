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
"""
import json

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import CreateView, UpdateView

from si.apps.siprof.models import Permissions
from si.sig_decorators import has_permission
from .forms import SottoIniziativaForm, GruppoForm, ListaIniziativeForm
from .models import Iniziativa, SottoIniziativa, Raggruppamento


# region INIZIATIVE
@has_permission(Permissions.APP_INIZIATIVE, Permissions.OP_READ)
def index(request):
    """
    INIZIATIVA : Indice generale ordinato per chiave primaria.
    """
    # Uso un form per gestire il controllo del gridview
    # lista_iniziative = Iniziativa.objects.filter(in_uso=True).order_by('pk')
    # context_dict = {'lista_iniziative': lista_iniziative, 'perm': perm}
    form = ListaIniziativeForm()

    # Popola il dizionario di interfaccia con la Griglia jqxGrid
    dj = {
        'url_add': reverse('corsi:add'),
        'url_del': reverse('corsi:del'),
        'url_edit': reverse('corsi:edit', kwargs={'pk': '12345'}),
        'url_detail': reverse('corsi:edit', kwargs={'pk': '12345'}),
        'sourcedata_url': '/si/corsi/api/get_corsi/',
        'sourcedata_max_row': 50,
        'sourcedata_data': """[
            {name: 'codice'},
            {name: 'denominazione'},
            {name: 'durata'},
            {name: 'ordine'},
            {name: 'pk'},
        ]""",
        'grid_columns': """[
            {text: 'Codice Corso', dataField: 'codice', width: "10%"},
            {text: 'Denominazione', dataField: 'denominazione', width: "70%"},
            {text: 'Durata', dataField: 'durata', width: "10%"},
            {text: 'Ordine', dataField: 'ordine', width: "10%"}
        ]"""
    }

    # Popola il dizionario per il template.
    context_dict = {'form': form, 'dj': dj}

    # Visualizza la risposta.
    return render(request, 'iniziative/index.html', context_dict)


class IniziativaAdd(CreateView):
    """
    INIZIATIVA : Creazione di una nuova iniziativa. !! Login required gestito in urls !!
    """
    model = Iniziativa
    template_name = 'iniziative/i_cu.html'
    success_url = '/si/iniziative/'
    fields = '__all__'


class IniziativaEdit(UpdateView):
    """
    INIZIATIVA : Modifica dei dati di un'iniziativa. !! Login required gestito in urls !!
    """
    template_name = 'iniziative/i_cu.html'
    model = Iniziativa
    success_url = '/si/iniziative/'
    fields = ['nome', 'descrizione', 'cup_cig', 'in_uso']


@login_required()
def iniziativa_delete(request, pk):
    """
    INIZIATIVA : Elimina l'iniziativa data se non ha figli.

    Non chiede conferma perchè la richiesta viene fatta a monte, prima di chiamare questa funzione.
    """
    # Cerca di recuperare l'iniziativa e se non ci riesce segnala errore.
    try:
        iniziativa = Iniziativa.objects.get(pk=pk)
    except Iniziativa.DoesNotExist:
        raise Http404("Indice iniziativa inesistente !")

    # Se l'iniziativa ha figli abbandona segnalando l'errore.
    if iniziativa.sottoiniziativa_set.count() > 0:
        context_dict = {'elemento': iniziativa,
                        'correlati': iniziativa.sottoiniziativa_set.all(),
                        'indietro': reverse('iniziative:index')}
        return render(request, 'e_delcorr.html', context_dict)

    # Altrimenti procede alla cancellazione.
    iniziativa.delete()
    return HttpResponseRedirect(reverse('iniziative:index'))


@login_required()
def detail(request, pk_iniziativa):
    """
    INIZIATIVA : Visualizzazione dei dettagli di un'iniziativa.
    """
    context_dict = {}

    try:
        # Recupero l'iniziativa da visualizzare.
        iniziativa = Iniziativa.objects.get(pk=pk_iniziativa)
        context_dict['iniziativa'] = iniziativa

        # Recupero tutte le sottoiniziative correlate.
        sottoiniziative = SottoIniziativa.objects.filter(iniziativa=pk_iniziativa)
        context_dict['sottoiniziative'] = sottoiniziative

    except Iniziativa.DoesNotExist:
        # Se l'Iniziativa non esiste arrivo qui in modo silente e con il dizionario vuoto per cui il template
        # visualizzerà : Nessuna iniziativa presente.
        pass

    # Visualizza il template.
    return render(request, 'iniziative/i_dtl.html', context_dict)
# endregion


# region SOTTO-INIZIATIVE
@login_required()
def sottoiniziativa_add(request, pk_iniziativa):
    """
    SOTTO-INIZIATIVA : Data un'iniziativa ci aggiunge una sotto iniziativa.
    """
    # Cerca di recuperare l'iniziativa e se non ci riesce segnala errore.
    try:
        iniziativa = Iniziativa.objects.get(pk=pk_iniziativa)
    except Iniziativa.DoesNotExist:
        raise Http404("Indice iniziativa inesistente !")

    # Legge i dati dal POST e li analizza per salvarli
    if request.method == 'POST':
        form = SottoIniziativaForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.iniziativa = iniziativa
            post.save()
            return HttpResponseRedirect(reverse('iniziative:detail', kwargs={'pk_iniziativa': pk_iniziativa}))
        else:
            print(form.errors)
    else:
        form = SottoIniziativaForm()

    # Popola il dizionario per il template.
    context_dict = {'form': form, 'iniziativa': iniziativa, 'blocktitle': 'Sotto Iniziativa', 'header':
                    'Sotto Iniziativa di ' + iniziativa.nome}

    # Visualizza il template.
    return render(request, 'si_cu_formasp_t1.html', context_dict)


@login_required()
def sottoiniziativa_edit(request, pk):
    """
    SOTTO-INIZIATIVA : Modifica dei dati della sotto iniziativa.
    """
    # Cerca di recuperare la sotto iniziativa e se non ci riesce segnala errore.
    try:
        sottoiniziativa = SottoIniziativa.objects.get(pk=pk)
    except SottoIniziativa.DoesNotExist:
        raise Http404("Indice sotto iniziativa inesistente !")

    # Legge i dati dal POST e li analizza per salvarli
    if request.method == 'POST':
        form = SottoIniziativaForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            sottoiniziativa.nome = post.nome
            sottoiniziativa.descrizione = post.descrizione
            sottoiniziativa.save()
            return HttpResponseRedirect(reverse('iniziative:detail',
                                                kwargs={'pk_iniziativa': sottoiniziativa.iniziativa.pk}))
        else:
            print(form.errors)
    else:
        form = SottoIniziativaForm(instance=sottoiniziativa)

    # Popola il dizionario per il template.
    context_dict = {'form': form, 'iniziativa': sottoiniziativa.iniziativa, 'blocktitle': 'Sotto Iniziativa', 'header':
                    'Sotto Iniziativa di : ' + sottoiniziativa.iniziativa.nome}

    # Visualizza il template.
    return render(request, 'si_cu_formasp_t1.html', context_dict)


@login_required()
def sottoiniziativa_delete(request, pk):
    """
    SOTTO-INIZIATIVA : Elimina la sotto iniziativa data se non ha figli.

    Non chiede conferma perchè la richiesta viene fatta a monte, prima di chiamare questa funzione.
    """
    # Cerca di recuperare l'iniziativa e se non ci riesce segnala errore.
    try:
        sottoiniziativa = SottoIniziativa.objects.get(pk=pk)
    except SottoIniziativa.DoesNotExist:
        raise Http404("Indice sotto-iniziativa inesistente !")

    # Se la sotto-iniziativa ha figli abbandona segnalando errore.
    if sottoiniziativa.raggruppamento_set.count() > 0:
        context_dict = {'elemento': sottoiniziativa,
                        'correlati': sottoiniziativa.raggruppamento_set.all(),
                        'indietro': reverse('iniziative:sub_detail', kwargs={'pk_sub': pk})}
        return render(request, 'e_delcorr.html', context_dict)

    # Altrimenti procede con la cancellazione e torna alla pagina di dettaglio dell'iniziativa padre.
    iniziativa = sottoiniziativa.iniziativa
    sottoiniziativa.delete()
    return HttpResponseRedirect(reverse('iniziative:detail', kwargs={'pk_iniziativa': iniziativa.pk}))


@login_required()
def sottoiniziativa_detail(request, pk_sub):
    """
    SOTTO-INIZIATIVA : Visualizzazione dei dettagli della sottoiniziativa.
    """
    context_dict = {}

    try:
        # Recupera la sottoiniziativa.
        sottoiniziativa = SottoIniziativa.objects.get(pk=pk_sub)
        context_dict['sottoiniziativa'] = sottoiniziativa

        # Recupera l'iniziativa padre.
        iniziativa = sottoiniziativa.iniziativa
        context_dict['iniziativa'] = iniziativa

        # Recupera la lista dei raggruppamenti
        raggruppamenti = Raggruppamento.objects.filter(sotto_iniziativa=pk_sub)
        context_dict['raggruppamenti'] = raggruppamenti

    except SottoIniziativa.DoesNotExist:
        # Se la sotto iniziativa non esiste non fa nulla in quanto il caso è già contemplato nel template.
        pass

    # Visualizza il template.
    return render(request, 'iniziative/sub_detail.html', context_dict)
# endregion


# region RAGGRUPPAMENTO
@login_required()
def gruppo_add(request, pk_sub):
    """
    GRUPPO : Data una sotto iniziativa ci aggiunge un gruppo.
    """
    # Cerca di recuperare la sotto iniziativa e se non ci riesce segnala errore.
    try:
        sottoiniziativa = SottoIniziativa.objects.get(pk=pk_sub)
    except SottoIniziativa.DoesNotExist:
        raise Http404("Indice sotto-iniziativa inesistente !")

    # Legge i dati dal POST e li analizza per salvarli
    if request.method == 'POST':
        form = GruppoForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.sotto_iniziativa = sottoiniziativa
            post.save()
            return HttpResponseRedirect(reverse('iniziative:sub_detail', kwargs={'pk_sub': pk_sub}))
        else:
            print(form.errors)
    else:
        form = GruppoForm()

    # Popola il dizionario per il template.
    context_dict = {'form': form, 'sottoiniziativa': sottoiniziativa, 'blocktitle': 'Raggruppamento', 'header':
                    'Raggruppamento di : ' + sottoiniziativa.nome}

    # Visualizza il template.
    return render(request, 'si_cu_formasp_t1.html', context_dict)


@login_required()
def gruppo_edit(request, pk):
    """
    GRUPPO : Modifica dei dati del gruppo.
    """
    # Cerca di recuperare il gruppo e se non ci riesce segnala errore.
    try:
        gruppo = Raggruppamento.objects.get(pk=pk)
    except Raggruppamento.DoesNotExist:
        raise Http404("Indice del raggruppamento inesistente !")

    # Legge i dati dal POST e li analizza per salvarli
    if request.method == 'POST':
        form = GruppoForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            gruppo.nome = post.nome
            gruppo.descrizione = post.descrizione
            gruppo.ordine = post.ordine
            gruppo.save()
            return HttpResponseRedirect(reverse('iniziative:sub_detail',
                                                kwargs={'pk_sub': gruppo.sotto_iniziativa.pk}))
        else:
            print(form.errors)
    else:
        form = GruppoForm(instance=gruppo)

    # Popola il dizionario per il template.
    context_dict = {'form': form, 'sottoiniziativa': gruppo.sotto_iniziativa, 'blocktitle': 'Raggruppamento', 'header':
                    'Raggruppamento di : ' + gruppo.sotto_iniziativa.nome}

    # Visualizza il template.
    return render(request, 'si_cu_formasp_t1.html', context_dict)


@login_required()
def gruppo_delete(request, pk):
    """
    GRUPPO : Elimina il raggruppamento.

    Non chiede conferma perchè la richiesta viene fatta a monte, prima di chiamare questa funzione.
    """
    # Cerca di recuperare la sotto-iniziativa e se non ci riesce segnala errore.
    try:
        raggruppamento = Raggruppamento.objects.get(pk=pk)
    except Raggruppamento.DoesNotExist:
        raise Http404("Indice raggruppamento inesistente !")

    # Procede con la cancellazione e torna alla pagina di dettaglio della sotto iniziativa padre.
    sottoiniziativa = raggruppamento.sotto_iniziativa
    raggruppamento.delete()
    return HttpResponseRedirect(reverse('iniziative:sub_detail', kwargs={'pk_sub': sottoiniziativa.pk}))


@login_required()
def gruppo_detail(request, pk_grp):
    """
    GRUPPO : Visualizzazione dei dettagli del Gruppo.
    """
    context_dict = {}

    try:
        # Recupera il gruppo.
        gruppo = Raggruppamento.objects.get(pk=pk_grp)
        context_dict['gruppo'] = gruppo

        # Recupera la sotto iniziativa padre.
        sottoiniziativa = gruppo.sotto_iniziativa
        context_dict['sottoiniziativa'] = sottoiniziativa

        # Recupera infine l'iniziativa radice
        iniziativa = sottoiniziativa.iniziativa
        context_dict['iniziativa'] = iniziativa

    except Raggruppamento.DoesNotExist:
        # Se il gruppo non esiste non fa nulla in quanto il caso è già contemplato nel template.
        pass

    # Visualizza il template.
    return render(request, 'iniziative/grp_detail.html', context_dict)
# endregion


# region API
@login_required()
def get_iniziative(request):
    results = []
    if request.is_ajax():
        # q = request.GET.get('term', '')
        iniziative = Iniziativa.objects.all()
        for iniziativa in iniziative:
            giano = dict()
            giano['pk'] = iniziativa.pk
            giano['nome'] = iniziativa.nome
            giano['descrizione'] = iniziativa.descrizione
            results.append(giano)
    else:
        results['data'] = 'fail'
    return JsonResponse(results, safe=False)


@login_required()
def get_sottoiniziative(request):
    print("Chiamata AJAX sotto iniziative")
    if request.is_ajax():
        pk = request.GET.get('pk', '')
        print('pk = ', pk)
        try:
            # Recupera la sottoiniziativa.
            sottoiniziative = SottoIniziativa.objects.filter(iniziativa=pk)

        except SottoIniziativa.DoesNotExist:
            # Se la sotto iniziativa non esiste non fa nulla in quanto il caso è già contemplato nel template.
            pass
        results = []
        for sottoiniziativa in sottoiniziative:
            stringa_json = {}
            stringa_json['text'] = sottoiniziativa.nome
            stringa_json['id'] = sottoiniziativa.pk
            results.append(stringa_json)
        data = json.dumps(results)
        print(data)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


@login_required()
def get_raggruppamenti(request):
    print("Chiamata AJAX raggruppamenti")
    if request.is_ajax():
        pk = request.GET.get('pk', '')
        print('pk = ', pk)
        try:
            # Recupera i raggruppamenti.
            raggruppamenti = Raggruppamento.objects.filter(sotto_iniziativa=pk)

        except Raggruppamento.DoesNotExist:
            # Se il raggruppamento non esiste non fa nulla in quanto il caso è già contemplato nel template.
            pass
        results = []
        for raggruppamento in raggruppamenti:
            stringa_json = {}
            stringa_json['text'] = raggruppamento.nome
            stringa_json['id'] = raggruppamento.pk
            results.append(stringa_json)
        data = json.dumps(results)
        print(data)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)
# endregion
