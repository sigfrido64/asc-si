# coding=utf-8
from si.apps.siprof.models import Profile
import json
__author__ = "Sig"


def permissions(request):
    """
    Se l'utente è loggato recupera la lista dei suoi permessi e la mette nel dizionario 'si_perms'.
    Il dizionario serve per tutti gli usi interni e nei templates per la produzione dei menu.
    La gestione degli accessi viene poi lasciata al decoratore della singola funzione.
    DIREI CHE ORMAI E' OBSOLETO VISTO CHE FACCIO TUTTO DIVERSAMENTE !

    :param request:
    :return:
    """
    # Se l'utente non è loggato riporta nulla.
    if not request.user.is_authenticated:
        return {'si_perms': False, 'si_user': False}
    user = Profile
    perms = request.user.profile.permissions
    return {'si_perms': perms, 'si_user': user}
