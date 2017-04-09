# coding=utf-8
__author__ = 'sig'
from django.conf.urls import patterns, url

urlpatterns = patterns('docusign.views',
    url(r'^lista/', 'lista', name='lista'),
)