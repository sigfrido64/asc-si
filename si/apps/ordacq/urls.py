# coding=utf-8
from django.conf.urls import url
from si.apps.ordacq.views import ordacq_create, ordacq_list, ordacq_update, ordacq_delete
from si.apps.ordacq.views import ordacq_export, ordacq_import
__author__ = 'Sig'


urlpatterns = [
    url(r'^$', ordacq_list, name='index'),
    url(r'^create/$', ordacq_create, name='create'),
    url(r'^export/$', ordacq_export, name='export'),
    url(r'^import/$', ordacq_import, name='import'),
    url(r'^(?P<pk>\d+)/update/$', ordacq_update, name='update'),
    url(r'^(?P<pk>\d+)/delete/$', ordacq_delete, name='delete'),
]
