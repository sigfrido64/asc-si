# coding=utf-8
from django.conf.urls import url
# from django.contrib.auth.decorators import login_required
from segnalazioni.views import index, corsobase_cu, corsobase_del, index_a, sega
__author__ = 'Sig'


urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^corsoedit/(?P<pk>\w+)$', corsobase_cu, name='corsobase_edit'),
    url(r'^corsoadd/$', corsobase_cu, name='corsobase_add'),
    url(r'^corsodel/(?P<pk>\w+)$', corsobase_del, name='corsobase_del'),

    url(r'^seg/(?P<pk>\w+)$', index_a, name='sega'),

    url(r'^sega/$', sega, name='sega'),
]
