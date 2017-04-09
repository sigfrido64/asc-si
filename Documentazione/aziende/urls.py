# coding=utf-8
from django.conf.urls import url
from .views import index, get_listanazioni, add_edit, get_listaziende
from .views import importanazioni, importaprovincie, importaaziende, importacontatti
__author__ = 'Sig'

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^add/$', add_edit, name='add'),
    url(r'^edit/(?P<pk>\w+)$', add_edit, name='edit'),
    # Sezione della API
    url(r'^api/get_listanazioni/$', get_listanazioni, name='get_listanazioni'),
    url(r'^api/2/$', get_listaziende),
    # Importazioni da Assocam
    url(r'^importa/nazioni/$', importanazioni, name='_i_nazioni'),
    url(r'^importa/provincie/$', importaprovincie, name='_i_provincie'),
    url(r'^importa/aziende/$', importaaziende, name='_i_aziende'),
    url(r'^importa/contatti/$', importacontatti, name='_i_contatti'),
]
