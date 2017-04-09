# coding=utf-8
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from .resources import OrdacqResource
from django.template.loader import render_to_string
from .models import TabellaStatoOrdini
from si.sig_decorators import has_permission
from si.apps.siprof.models import Profile
from .forms import TabellaStatoOrdiniForm
from tablib import Dataset

# Definisco qui il nome dell'applicazione come lo voglio nel Data Base in modo che sia uguale per tutte le viste.
THIS_APP = Profile.APP_ORDACQ


@has_permission(THIS_APP, Profile.OP_READ)
def ordacq_list(request):
    """
    Genera la vista con la lista della tabella stato ordini.
    ATTENZIONE che app deve contenere il nome dell'applicazione per la corretta gestione dei permessi quando vado
    a compilare il corpo delle tabelle.
    """
    ordacq = TabellaStatoOrdini.objects.all()
    return render(request, 'ordacq/ordacq_list.html', {'ordacq_list': ordacq, 'app': THIS_APP})


def partial_ordacq_list(request):
    """
    Riporta il dizionario con la lista degli ordini di acquisto per il rendering sul template.
    
    :param request: Oggetto 'request' della vista da cui parto.
    :return: Il dizionario completo da riportare via JsonResponse
    """
    data = dict()
    data['form_is_valid'] = True
    ordacq = TabellaStatoOrdini.objects.all()
    data['html_ordacq_list'] = render_to_string('ordacq/includes/partial_ordacq_list.html', {
        'ordacq_list': ordacq, 'app': THIS_APP}, request=request)
    return data


def save_ordacq_form(request, form, template_name):
    """
    Salva il form e rinfresca la tabella generale. Uso questa che è sostanzialmente comune alle due voci di Update
    e Create così da poter gestire correttamente i permessi.
    """
    data = dict()
    # Se ho dei dati da salvare e sono validi li salvo e ripreparo la lista degli items per il refresh.
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return JsonResponse(partial_ordacq_list(request))
        else:
            data['form_is_valid'] = False
    # Altrimenti propongo il form vuoto.
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


@has_permission(THIS_APP, Profile.OP_ADD)
def ordacq_create(request):
    """
    Aggiungo un elemento alla lista degli ordini.
    """
    if request.method == 'POST':
        form = TabellaStatoOrdiniForm(request.POST)
    else:
        form = TabellaStatoOrdiniForm()
    return save_ordacq_form(request, form, 'ordacq/includes/partial_ordacq_create.html')


@has_permission(THIS_APP, Profile.OP_UPDATE)
def ordacq_update(request, pk):
    """
    Aggiorno un elemento della lista degli ordini.
    """
    book = get_object_or_404(TabellaStatoOrdini, pk=pk)
    if request.method == 'POST':
        form = TabellaStatoOrdiniForm(request.POST, instance=book)
    else:
        form = TabellaStatoOrdiniForm(instance=book)
    return save_ordacq_form(request, form, 'ordacq/includes/partial_ordacq_update.html')


@has_permission(THIS_APP, Profile.OP_DELETE)
def ordacq_delete(request, pk):
    """
    Cancello un item.
    La richiesta della conferma la trovo direttamente nel form.
    """
    ordacq = get_object_or_404(TabellaStatoOrdini, pk=pk)
    data = dict()
    if request.method == 'POST':
        ordacq.delete()
        return JsonResponse(partial_ordacq_list(request))
    else:
        context = {'ordacq': ordacq}
        data['html_form'] = render_to_string('ordacq/includes/partial_ordacq_delete.html',
                                             context, request=request)
    return JsonResponse(data)


@has_permission(THIS_APP, Profile.OP_EXPORT)
def ordacq_export(request):
    """
    Esporta la tabella in formato Excel.
    """
    ordacq_resource = OrdacqResource()
    dataset = ordacq_resource.export()
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Aquisti.xls"'
    return response


@has_permission(THIS_APP, Profile.OP_IMPORT)
def ordacq_import(request):
    """
    Importa un file Excel con la lista degli Acquisti.
    """
    data = dict()
    if request.method == 'POST':
        ordacq_resource = OrdacqResource()
        dataset = Dataset()
        print("Prima di accedere a Myfile")
        new_ordacq = request.FILES['myfile']

        imported_data = dataset.load(new_ordacq.read(), 'xls')
        result = ordacq_resource.import_data(dataset, dry_run=True)  # Test the data import
        if not result.has_errors():
            ordacq_resource.import_data(dataset, dry_run=False)  # Actually import now

        # return JsonResponse(partial_ordacq_list(request))
        return redirect('ordacq:index')
    else:
        context = dict()
        data['html_form'] = render_to_string('ordacq/includes/partial_ordacq_import.html',
                                             context, request=request)
    return JsonResponse(data)
    #return render(request, 'ordacq/includes/partial_ordacq_import.html', context)

