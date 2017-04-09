# coding=utf-8
from si.apps.siprof.models import Profile
import json
__author__ = "Sig"


def permissions(request):
    """
    Se l'utente è loggato recupera la lista dei suoi permessi e la mette nel dizionario 'si_perms'.
    Il dizionario serve per tutti gli usi interni E NEI TEMPLATES per la produzione dei menu !!!
    Occhio che li non lo vedi e non te ne ricordi più dopo !
    La gestione degli accessi viene poi lasciata al decoratore della singola funzione.
    

    :param request:
    :return:
    """
    # Se l'utente non è loggato riporta nulla.
    if not request.user.is_authenticated:
        return {'si_perms': False, 'si_user': False}
    user = Profile
    perms = request.user.profile.permissions
    return {'si_perms': perms, 'si_user': user}
