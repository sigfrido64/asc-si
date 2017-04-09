# coding=utf-8

from django.conf.urls import url

from .views import index, get_corsi, add_edit, corso_del
from .views import lezioni_getall, lezione_add, lezione_upd, lezione_del


urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^add/$', add_edit, name='add'),
    url(r'^edit/(?P<pk>\w+)$', add_edit, name='edit'),
    url(r'^detail/(?P<pk>\w+)$', add_edit, name='detail'),
    url(r'^api/get_corsi/$', get_corsi, name='get_corsi'),
    url(r'^api/del_corso/$', corso_del, name='del'),
    url(r'^api/lezioni_getall', lezioni_getall, name='lezioni_getall'),
    url(r'^api/lezione_add/$', lezione_add, name='lezione_add'),
    url(r'^api/lezione_upd', lezione_upd, name='lezione_upd'),
    url(r'^api/lezione_del', lezione_del, name='lezione_del'),
]
