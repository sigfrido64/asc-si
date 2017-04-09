# coding=utf-8
from django.contrib import admin
from .models import Iniziativa, SottoIniziativa, Raggruppamento


# Register your models here.
admin.site.register(Iniziativa)
admin.site.register(SottoIniziativa)
admin.site.register(Raggruppamento)

