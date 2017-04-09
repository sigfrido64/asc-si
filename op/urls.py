# coding=utf-8
from django.conf.urls import url
from .views import index, op_edit, op_getlist


urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^add/$', op_edit, name='add'),
    url(r'^edit/(?P<pk>\w+)$', op_edit, name='edit'),

    url(r'^api/op_getlist$', op_getlist, name='op_getlist'),
]
