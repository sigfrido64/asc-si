# coding=utf-8
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from .views import index, logout_view
from django.contrib.auth.views import login, password_change


urlpatterns = [
    url(r'^si/$', index, name="index"),
    url(r'^si/ordacq/', include('si.apps.ordacq.urls', namespace='ordacq', app_name='ordacq')),
    
    # Qui ci sono le parti vecchie
    url(r'^si/login/$', login, name='login'),
    url(r'^si/logout/$', logout_view, name='logout'),
    url(r'^si/passchange/$', password_change, {'post_change_redirect': '/si/'}),
    url(r'^admin/', include(admin.site.urls)),
 
] + static(settings.SIFILEDATA_URL, document_root=settings.SIFILEDATA_ROOT)
# url(r'^si/segnalazioni/', include('segnalazioni.urls', namespace="segnalazioni", app_name="segnalazioni")),

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]


"""
   url(r'^si/iniziative/', include('iniziative.urls', namespace="iniziative", app_name="iniziative")),
    url(r'^si/fs/', include('sifilesmanager.urls', namespace="fs", app_name="fs")),
    url(r'^si/corsi/', include('corsi.urls', namespace="corsi", app_name="corsi")),
    
    url(r'^si/op/', include('op.urls', namespace="op", app_name="op")),
    url(r'^si/aziende/', include('aziende.urls', namespace="aziende", app_name="aziende"))
"""