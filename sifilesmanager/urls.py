# -*- coding: utf-8 -*-
from django.conf.urls import url
from sifilesmanager.views import index, fileupload, folder_add, folder_edit, folder_delete, file_delete
__author__ = 'Sig'


urlpatterns = [
    url(r'^(?P<pk>\d+|None)$', index, name='index'),
    url(r'^$', index, name='index'),
    url(r'^up/$', fileupload, name='upload'),
    url(r'^up/(?P<pk>\d+)$', fileupload, name='upload'),
    url(r'^folderadd/(?P<inodenumber>\d+|None)$', folder_add, name='folder_add'),
    url(r'^folderedit/(?P<pk>\d+)$', folder_edit, name='folder_edit'),
    url(r'^folderdelete/(?P<pk>\d+)$', folder_delete, name='folder_delete'),
    url(r'^filedelete/(?P<pk>\d+)$', file_delete, name='file_delete'),
]

