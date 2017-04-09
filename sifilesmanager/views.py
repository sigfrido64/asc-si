# -*- coding: utf-8 -*-
# Create your views here.
from .forms import SiFileForm, INodeForm
from .models import SiFile
from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from .models import INode
from django.conf import settings
import os


# region FILES
def inodeslista(nodopadre=None):
    """
    Dato un nodo padre mi da la lista delle cartelle e dei files contenuti al suo interno.
    """
    lista_inodes = INode.objects.filter(padre=nodopadre).order_by('nome')
    lista_files = SiFile.objects.filter(inode=nodopadre).order_by('nome')

    dizionario = {'lista_inodes': lista_inodes, 'lista_files': lista_files}
    return dizionario


@login_required()
def index(request, pk=None):
    """
    Radice del File System, inizio navigazione.
    """
    # Recupero la lista dei files e delle directory qui presenti.
    lista_inodes = INode.objects.filter(padre=pk).order_by('nome')
    lista_files = SiFile.objects.filter(inode=pk).order_by('nome')

    # Preparo il link per salire di un livello considerando il livello radice quello con padre None.
    if pk is None:
        su = reverse('fs:index')        # Genero il link per salire di un livello
        up = reverse('fs:upload')       # Genero il link per l'upload
    else:
        up = reverse('fs:upload', kwargs={'pk': pk})
        inode_appoggio = INode.objects.get(pk=pk)
        inode_su = inode_appoggio.padre
        if inode_su is None:
            su = reverse('fs:index')
        else:
            su = reverse('fs:index', kwargs={'pk': inode_su.pk})

    # Compongo il dizionario.
    context_dict = {'lista_inodes': lista_inodes, 'lista_files': lista_files, 'nodo': pk, 'su': su, 'up': up}

    # Visualizzo la risposta.
    return render(request, 'sifilesmanager/fs_index.html', context_dict)


@login_required
def fileupload(request, pk=None):
    """
    Carica un file nel sistema.
     Controlla se l'inode passato è valido altrimenti segnala errore
    print("pk = ", pk)
    inode = None
    if pk != 'None':
        try:
            inode = INode.objects.get(pk=pk)
        except INode.DoesNotExist:
            raise Http404("INode inesistente ! Cosa stai combinando ?")
    """

    # Verifico se l'inode esiste altrimenti segnalo errore.
    if pk is None:
        inode = None
    else:
        try:
            inode = INode.objects.get(pk=pk)
        except INode.DoesNotExist:
            raise Http404("INode inesistente ! Cosa stai combinando ?")

    if request.method == 'POST':
        form = SiFileForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = SiFile(filename=request.FILES['filename'], descrizione=request.POST['descrizione'], inode=inode)
            newdoc.save()
            return HttpResponse('<script type="text/javascript">window.opener.location.reload(false); \
                window.close();</script>')
        else:
            print(form.errors)
    else:
        form = SiFileForm()

    # Popola il dizionario per il template. Occhio che metto anche 'pk' altrimenti poi diventi scemo !
    context_dict = {'form': form, 'pk': pk}

    # Visualizza il template.
    return render(request, 'sifilesmanager/fs_upload.html', context_dict)


@login_required()
def file_delete(request, pk):
    """
    FILE : Elimina il file.
    """
    # Cerca di recuperare i dati del file e se non ci riesce segnala errore.
    try:
        sifile = SiFile.objects.get(pk=pk)
    except SiFile.DoesNotExist:
        raise Http404("File inesistente !")

    # Se è un POST vuol dire che ci sono già passato e che ho confermato la cancellazione, quindi eseguo.
    if request.method == 'POST':
        radice = settings.SIFILEDATA_ROOT
        filefisico = os.path.join(radice, sifile.pathurl, sifile.url)
        os.remove(filefisico)
        sifile.delete()
        return HttpResponse('<script type="text/javascript">window.opener.location.reload(false); \
                window.close();</script>')
    else:
        # Altrimenti visualizzo il form con la domanda se voglio cancellare.
        context_dict = {'sifile': sifile}
        return render(request, 'sifilesmanager/file_del.html', context_dict)
# endregion


# region FOLDERS
@login_required()
def folder_add(request, inodenumber):
    """
    FOLDER : Dato una cartella ne crea una all'interno.
    """
    # Cerca di recuperare l'inode e se non ci riesce segnala errore.
    inode = None
    if inodenumber != 'None':
        try:
            inode = INode.objects.get(pk=inodenumber)
        except INode.DoesNotExist:
            raise Http404("INode inesistente !")

    # Legge i dati dal POST e li analizza per salvarli
    if request.method == 'POST':
        form = INodeForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.padre = inode
            post.save()
            return HttpResponse('<script type="text/javascript">window.opener.location.reload(false); \
                window.close();</script>')
        else:
            print(form.errors)
    else:
        form = INodeForm()

    # Popola il dizionario per il template.
    context_dict = {'form': form, 'inodenumber': inodenumber}

    # Visualizza il template.
    return render(request, 'sifilesmanager/folder_cu.html', context_dict)


@login_required()
def folder_edit(request, pk):
    """
    FOLDER : Modifica dei dati della cartella.
    """
    # Cerca di recuperare i dati del folder e se non ci riesce segnala errore.
    try:
        inode = INode.objects.get(pk=pk)
    except INode.DoesNotExist:
        raise Http404("INode inesistente !")

    # Legge i dati dal POST e li analizza per salvarli
    if request.method == 'POST':
        form = INodeForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            inode.nome = post.nome
            inode.descrizione = post.descrizione
            inode.save()
            return HttpResponse('<script type="text/javascript">window.opener.location.reload(false); \
                window.close();</script>')
        else:
            print(form.errors)
    else:
        form = INodeForm(instance=inode)

    # Popola il dizionario per il template.
    context_dict = {'form': form, 'pk': pk}

    # Visualizza il template.
    return render(request, 'sifilesmanager/folder_cu.html', context_dict)


@login_required()
def folder_delete(request, pk):
    """
    FOLDER : Elimina la cartella se è vuota.
    """
    # Cerca di recuperare i dati del folder e se non ci riesce segnala errore.
    try:
        inode = INode.objects.get(pk=pk)
    except INode.DoesNotExist:
        raise Http404("INode inesistente !")

    # Ora controllo se il folder ne contiene altri.
    if inode.inode_set.count() > 0:
        return HttpResponse('<script type="text/javascript">alert("La cartella non può essere cancellata perchè non è vuota !"); \
            window.close();</script>')

    # Se è un POST vuol dire che ci sono già passato e che ho confermato la cancellazione, quindi eseguo.
    if request.method == 'POST':
        # padre = inode.padre
        inode.delete()
        return HttpResponse('<script type="text/javascript">window.opener.location.reload(false); \
                window.close();</script>')
    else:
        # Altrimenti visualizzo il form con la domanda se voglio cancellare.
        context_dict = {'folder': inode}
        return render(request, 'sifilesmanager/folder_del.html', context_dict)
# endregion
