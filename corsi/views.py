# coding=utf-8
import json

from bson.objectid import ObjectId
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

# from sigutil import get_obj_or_404, hashsig
from si.apps.siprof.models import Permissions
from si.sig_decorators import has_permission
from sigutil import hashsig
from .forms import CorsoForm
from .models import Corso, Lezione, CartelleCorsoTask


def task_dispatcher(corso, vecchio_stato, nuovo_stato):
    # Passaggio da BOZZA a ...
    if vecchio_stato == 0:
        # PIANIFICATO : Emissione della richiesta di creazione della cartella corso.
        if nuovo_stato == 10:
            newtask = CartelleCorsoTask()
            newtask.corso = corso
            newtask.anno_formativo = "2015-2016"  # TODO Questo deve arrivare dal corso
            newtask.tipologia = "FAP"    # TODO Questo deve arrivare dal corso
            newtask.save()
    return


@has_permission(Permissions.APP_CORSI, Permissions.OP_READ)
def index(request):
    """
    Lista dei corsi in ordine alfabetico
    :param request:
    """
    """
    # Questo sarà il cuore del decorator che userò qui.
    permissions = request.user.userpermissions.permissions
    if UserPermissions.APP_INIZIATIVE not in permissions:
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied
    """
    """
    if UserPermissions.APP_INIZIATIVE not in si_perm:
        return Http404"""
    # Verifico se l'utente ha il permesso di usare questa vista.
    #perm = get_object_or_404(UserPermissions, user=request.user, item='iniziative')
    #if not perm:
    #    return Http404

    # print(request.si_perms)

    # Recupero la lista dei corsi.
    lista_corsi = Corso.objects().order_by('codice_corso')
    # context_dict = {'lista_corsi': lista_corsi, 'perm': perm}
    context_dict = {'lista_corsi': lista_corsi}

    # Visualizza la risposta.
    return render(request, 'corsi/index.html', context_dict)


@login_required()
def add_edit(request, pk=None):
    """
    Aggiunge o edita un corso.
    :param pk: Id del corso che voglio editare, se non è presente è un inserimento.
    :param request:
    """
    # Se l'utente non è abilitato esce.
    perm = get_object_or_404(Permissions, user=request.user.get_username())
    if Permissions.CORSI_ALL not in perm.permissions:
        return Http404

    # Se è specificata una pk prova a recuperare il record altrimenti si tratta di un inserimento e procedo oltre.
    if pk:
        corso = get_obj_or_404(Corso, codice_edizione=pk)
    else:
        corso = Corso()

    if request.method == 'POST':
        form = CorsoForm(request.POST, instance=corso)
        if form.is_valid():
            print("Form valido !")
            """
            # Se si tratta di un aggiornamento valuto eventuali azioni.
            if pk:
                corso_old = get_obj_or_404(Corso, codice_edizione=pk)
                task_dispatcher(corso=corso_old.pk, vecchio_stato=corso_old.stato,
                                nuovo_stato=form.cleaned_data.get('stato'))
            """
            form.save()
            # post.save()
            return HttpResponseRedirect(reverse('corsi:index'))
        else:
            print("Macchecazzo")
            print(form.errors)
    else:
        form = CorsoForm(instance=corso)

    # Popola il dizionario per il template.
    context_dict = {'form': form, 'perm': perm}

    # Visualizza il template.
    return render(request, 'corsi/add_edit.html', context_dict)


"""
In modo più purista sarebbe !
E sarebbe anche più semplice !
def edit(request, id=None, template_name='article_edit_template.html'):
    if id:
        article = get_object_or_404(Article, pk=id)
        if article.author != request.user:
            return HttpResponseForbidden()
    else:
        article = Article(author=request.user)

    form = ArticleForm(request.POST or None, instance=article)
    if request.POST:
        if form.is_valid():
            form.save()

            # If the save was successful, redirect to another page
            redirect_url = reverse(article_save_success)
            return HttpResponseRedirect(redirect_url)

    return render_to_response(template_name, {
        'form': form,
    }, context_instance=RequestContext(request))
"""

# region Corsi Ajax API.
@csrf_exempt
def get_corsi(request):
    """
    :param request: Header della richiesta dal server.
    :return: Lista completa di tutti i corsi.
    TODO : Il limite lo devo ricevere come parametro dalla pagina web !
    """
    results = []
    if request.is_ajax():
        filtro = hashsig(request.GET.get('filtro', ''))
        corsi = Corso.objects(codice_edizione__contains=filtro)[:50]
        for corso in corsi:
            corsi_json = dict()
            corsi_json['pk'] = corso.pk
            corsi_json['codice'] = corso.codice_edizione
            corsi_json['denominazione'] = corso.denominazione
            corsi_json['durata'] = corso.durata
            corsi_json['ordine'] = "Ciccio"
            results.append(corsi_json)
    else:
        results['data'] = 'fail'
    return JsonResponse(results, safe=False)


@csrf_exempt
def corso_del(request):
    """
    :param request: Header della richiesta dal server.
    :return: Lista completa di tutti i corsi.
    TODO : Il limite lo devo ricevere come parametro dalla pagina web !
    """
    # results = []
    if request.is_ajax():
        print("Sono in cancellazione di un corso !")
        id_corso = request.POST.get('pk', '')
        print("Corso : " + id_corso)
        results = {'status': 'error', 'message': 'pirla'}
    else:
        results = {'status': 'error'}
    return JsonResponse(results, safe=False)

# endregion


# region Lezioni Ajax API.
def lezioni_getall(request):
    """
    Recupera una lista non ordinata delle lezioni associate ad un dato corso.

    :param request: 'corso' : codice di edizione del corso di cui voglio recuperare le lezioni.
    :return: Lista delle lezioni associate al corso.
    """
    # Recupero il corso se esiste.
    corso = request.GET.get('corso', '')
    corso = get_obj_or_404(Corso, codice_edizione=corso)

    # Itero sulle lezioni
    results = []
    for lezione in corso.lezioni:
        lezione_json = {}
        lezione_json['id'] = str(lezione.id)
        lezione_json['data'] = lezione.data
        lezione_json['inizio'] = lezione.inizio
        lezione_json['fine'] = lezione.fine
        lezione_json['ore'] = lezione.ore
        lezione_json['sede'] = lezione.sede

        results.append(lezione_json)

    data = json.dumps(results)
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def lezione_add(request):
    """
    Aggiunge una lezione ad un dato corso.

    :param request: 'corso' : codice di edizione del corso cui aggiungo una lezione.
    :return: 'success' : 'true' in caso di successo.
    """

    # Recupero il corso se esiste.
    corso = request.GET.get('corso', '')
    corso = get_obj_or_404(Corso, codice_edizione=corso)

    # Creo la nuova lezione.
    lezione = Lezione()
    lezione.id = ObjectId()
    lezione.data = request.GET.get('data', '')
    lezione.inizio = request.GET.get('inizio', '')
    lezione.fine = request.GET.get('fine', '')
    lezione.sede = request.GET.get('sede', '')

    # Appendo al corso.
    corso.lezioni.append(lezione)
    corso.save()

    # Riporta OK.
    results = [{'success': 'true'}]

    data = json.dumps(results)
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def lezione_upd(request):
    """
    Modifica i dati di una particolare lezione.

    :param request: 'corso' : codice di edizione del corso di cui sto modificando una lezione.
                    'lezID' : id della lezione che sto modificando.
                    'data' : Nuova data della lezione.
                    'inizio' : Nuova ora di inizio della lezione.
                    'fine' : Nuova ora di fine della lezione.
    :return: 'success' : 'true' in caso di successo.
    """
    # Recupero il corso se esiste.
    corso = request.GET.get('corso', '')
    corso = get_obj_or_404(Corso, codice_edizione=corso)
    print("Corso recuperato")

    # Recupero l'id della lezione e la cerco nel DocumentEmbedded del corso.
    lezid = request.GET.get('lezID', '')
    lezione = next((lezione for lezione in corso.lezioni if str(lezione.id) == lezid), None)

    # A questo punto aggiorno i campi con quelli del form.
    lezione.data = request.GET.get('data', '')
    lezione.inizio = request.GET.get('inizio', '')
    lezione.fine = request.GET.get('fine', '')
    lezione.sede = request.GET.get('sede', '')

    # Salvo il tutto.
    corso.save()

    # Riporta OK.
    results = [{'success': 'true'}]

    data = json.dumps(results)
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def lezione_del(request):
    """
    Elimina la lezione dal corso indicato.

    :param request: 'corso' : codice di edizione del corso da cui sto eliminando una lezione.
                    'lezID' : id della lezione che sto eliminando.
    :return: 'success' : 'true' in caso di successo.
    """
    # Recupero il dati del codice di edizione del corso e della lezione.
    corso = request.GET.get('corso', '')
    lezid = request.GET.get('id', '')

    # Elimino la lezione indicata dal corso in oggetto.
    Corso.objects(codice_edizione=corso).update_one(pull__lezioni__id=Lezione(id=lezid).id)

    # Riporto ok.
    results = [{'success': 'true'}]
    data = json.dumps(results)

    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

# endregion
