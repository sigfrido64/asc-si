# coding=utf-8

from django.http import HttpResponse


def index(request):
    """
    Vista di Prova !
    :param request:
    :return:
    """
    print(request)
    return HttpResponse("Rango says hey there world!")