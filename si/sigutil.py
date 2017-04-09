# coding=utf-8
from django.http import Http404
from tasker.models import Heartbeats
import datetime
import re
from django.conf import settings
from django.shortcuts import get_object_or_404


def get_obj_or_404(klass, *args, **kwargs):
    """
    :param klass: Classe Modello per cui voglio richiamare un elemento.
    :param args: Argomenti della chiamata per il filtro del record.
    :return: L'oggetto corrispondente al criterio di selezione che ho passato come parametro o Http404 se
            la classe non esiste proprio.
    """
    try:
        return klass.objects.get(*args, **kwargs)
    except klass.DoesNotExist:
        raise Http404()


def heartbeat(processo, timeout):
    """
    Gestisce

    :param processo: Nome del processo che sto monitorando
    :param timeout: Timeout in secondi trascorso il quale si deve pensare che il processo sia abortito
    :return: Nulla. Tutti i dati vengono salvati nel data base di appoggio.
    """
    hb = Heartbeats()
    hb.processo = processo
    hb.timeout = timeout
    hb.data_aggiornamento = datetime.datetime.now()
    hb.save()


def stampadebug(messaggio):
        """
        Stampa un messaggio di debug.

        :param messaggio: il messaggio da stampare se DEBUG_PRINT è True, altrimenti non fa nulla.
        :param debug_flag: flag che dice se devo o meno stampare il messaggio. In questo modo posso abilitare la
                           stampa di debug per il singolo modulo.
        :return: None
        """
        if settings.DEBUG_PRINT:
            print(messaggio)


def concatena(*args):
    """
    Concatena un numero arbitratrio di stringhe anche se sono nulle e potrebbero portare ad errori di run-time
    :param args:
    :return:
    """
    linea = ''
    for l in args:
        linea += str(l if l else '')
    return linea


def valid_email(email):
    """
    Verifica se una e-mail può essere considerata formalmente valida.

    :param email: La mail da controllare.
    :return: True se valida, False altrimenti.
    """
    email_regex = re.compile(
        # dot-atom
        r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"
        # quoted-string
        r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-011\013\014\016-\177])*"'
        # domain (max length of an ICAAN TLD is 22 characters)
        r')@(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}|[A-Z0-9-]{2,}(?<!-))$', re.IGNORECASE
    )

    return email_regex.match(email)


def hashsig(linea):
    return re.sub('[^0-9a-zA-Z]+', '', linea).upper()


"""
PROFILAZIONE
    # Includes
    import cProfile, pstats, io

    # Inizio Profilazione
    pr = cProfile.Profile()
    pr.enable()

    # Fine Profilazione e stampa risultati
    pr.disable()
    f = open("profile.txt", "w", encoding="utf-8")
    sortby = 'cumulative'
    ps = pstats.Stats(pr, stream=f).sort_stats(sortby)
    ps.print_stats()
"""

