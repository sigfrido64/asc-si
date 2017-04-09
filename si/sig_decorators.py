# coding=utf-8
from django.conf import settings
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
__author__ = "Sig"


def has_permission(app, azione):
    """
    Definisco il decoratore che mi serve per controllare se l'utente è autorizzato ad accedere ad una data vista
    sulla base dei parametri che fornisco.
    Entambi i parametri devono fare riferimento alla classe UserPermission per evitare di usare delle costanti
    fuori di qui.
    Uso questa sintassi perchè voglio un decoratore con i parametri.
    
    :param app: Nome dell'applicazione su cui controllo il permesso (ad es. 'iniziative').
    :param azione: Azione che voglio compiere (ad es. 4).
    :return: Se non sono autorizzato solleva l'eccezione PermissionDenied altrimenti esegue la vista normalmente.
    """
    def real_decorator(function):
        def wrap(request, *args, **kwargs):
            # Come prima cosa devo controllare se è loggato, in caso contrario mi manda alla pagina di login.
            if not request.user.is_authenticated:
                return redirect(settings.LOGIN_URL)
            # Gira la richiesta di autorizzazione alla funzione che ho nel modello così tutto il processo di
            # controllo rimane circoscritto a lui.
            if request.user.profile.is_authorized(app, azione):
                # Se mi da ok eseguo la vista.
                return function(request, *args, **kwargs)
            else:
                raise PermissionDenied

        wrap.__doc__ = function.__doc__
        wrap.__name__ = function.__name__
        return wrap
    return real_decorator

