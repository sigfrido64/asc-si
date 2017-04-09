"""
    In questo esempio vado a compilare dei dizionari con cui mi interfaccio con delle routines in Javascript che
    poi fanno tutto il lavoro lato Client.
"""

@has_permission(THIS_APP, Permissions.OP_READ)
def index(request):
    """
    Genera la vista con la lista della tabella stato ordini.
    Qui uso la griglia Jqx per cui buona parte del lavoro la fa il relativo file in includes.
    """
    # Popola il dizionario di interfaccia con la Griglia jqxGrid
    dj = {
        'url_detail': reverse('corsi:edit', kwargs={'pk': '12345'}),
        'sourcedata_url': reverse('ordacq:api_get_tabella_acquisti'),
        'sourcedata_max_row': 50,
        'sourcedata_data': """[
                { name: 'protocollo'},
                { name: 'data'},
                { name: 'pk'},
            ]""",
        'grid_columns': """[
                { text: 'N. Prot.', dataField: 'protocollo', width: "10%"},
                { text: 'Data Ordine', dataField: 'data', width: "70%"},
            ]"""
    }
    # Adesso aggiungo le varie voci di menù se sono autorizzato dai permessi.
    actual_perm = request.user.permissions
    if actual_perm.is_authorized(THIS_APP, Permissions.OP_ADD):
        dj['url_add'] = reverse('corsi:add')
    if actual_perm.is_authorized(THIS_APP, Permissions.OP_DEL):
        dj['url_del'] = reverse('corsi:del')
    if actual_perm.is_authorized(THIS_APP, Permissions.OP_EDIT):
        dj['url_edit'] = reverse('corsi:edit', kwargs={'pk': '12345'})
    
    # Popola il dizionario per il template.
    context_dict = {'dj': dj}
    return render(request, 'ordacq/index.html', context_dict)
