# coding=utf-8
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from iniziative.views import IniziativaAdd, IniziativaEdit, index, detail, sottoiniziativa_detail, \
    sottoiniziativa_add, sottoiniziativa_edit, gruppo_add, gruppo_edit, gruppo_detail, \
    iniziativa_delete, sottoiniziativa_delete, gruppo_delete, get_iniziative, get_sottoiniziative, \
    get_raggruppamenti
__author__ = 'Sig'


urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^add/$', login_required(IniziativaAdd.as_view()), name='add'),
    url(r'^edit/(?P<pk>\d+)$', login_required(IniziativaEdit.as_view()), name='edit'),
    url(r'^delete/(?P<pk>\d+)$', iniziativa_delete, name='delete'),
    url(r'^(?P<pk_iniziativa>\d+)/$', detail, name='detail'),

    url(r'^api/get_iniziative/$', get_iniziative, name='get_iniziative'),
    url(r'^api/get_sottoiniziative$', get_sottoiniziative, name='get_sottoiniziative'),
    url(r'^api/get_raggruppamenti$', get_raggruppamenti, name='get_raggruppamenti'),

    url(r'^(?P<pk_iniziativa>\d+)/subadd/$', sottoiniziativa_add, name='sub_add'),
    url(r'^subedit/(?P<pk>\d+)$', sottoiniziativa_edit, name='sub_edit'),
    url(r'^delete_sub/(?P<pk>\d+)$', sottoiniziativa_delete, name='sub_delete'),
    url(r'^sub/(?P<pk_sub>\d+)/$', sottoiniziativa_detail, name='sub_detail'),

    url(r'^(?P<pk_sub>\d+)/grpadd/$', gruppo_add, name='grp_add'),
    url(r'^grpedit/(?P<pk>\d+)$', gruppo_edit, name='grp_edit'),
    url(r'^delete_grp/(?P<pk>\d+)$', gruppo_delete, name='grp_delete'),
    url(r'^grp/(?P<pk_grp>\d+)/$', gruppo_detail, name='grp_detail'),
]


