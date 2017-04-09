# coding=utf-8
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout
__author__ = "Sig"


@login_required
def index(request):
    """
    Visualizzo il form iniziale.
    TODO : Rivedere come cambia con nuovo toolbar !

    :param request: Handle della richiesta
    :return: Mi manda alla pagina iniziale che potrebbe essere diversa a seconda dell'utente.
    """
    # Visualizzo il form iniziale.
    context_dict = {}
    return render(request, 'index.html', context_dict)


def logout_view(request):
    logout(request)
    return redirect('login')
