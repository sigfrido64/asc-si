# coding=utf-8
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db.models.signals import post_save
from django.dispatch import receiver

"""
    Qui gestisco la profilazione degli utenti andando a definire le applicazioni del progetto ed i vari tipi di
    permessi che posso avere sulle stesse.
"""


class Profile(models.Model):
    # Queste sono le voci degli applicativi che voglio autorizzare.
    # Attenzione che ogniuna di queste DEVE prevedere una voce di permesso per ogni azienda su cui vado ad operare
    # per dire che sono esplicitamente autorizzato a farlo.
    # Ad es. per azienda = 'asc' avrò : 'asc.aziende' come voce di dizionario cui fare riferimento.
    APP_AZIENDE = 'aziende'
    APP_CORSI = 'corsi'
    APP_INIZIATIVE = 'iniziative'
    APP_ORDACQ = 'ordacq'
    
    __SYSAPP = ()

    # Questi sono i permessi.
    OP_READ = 1
    OP_ADD = 2
    OP_UPDATE = 4
    OP_DELETE = 8
    OP_EXPORT = 16
    OP_IMPORT = 32

    # Definizione dei campi del modello.
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    permissions = JSONField(null=True)
    azienda = models.CharField(max_length=10, default='asc', verbose_name="Azienda su cui l'utente sta operando.")

    # Gestione dei segnali che lo rendono un'estensione del modello generale dell'utente.
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def is_authorized(self, app, azione):
        """
        Mi dice se l'utente in questione è autorizzato a svolgere l'azione definita da perm sull'applicazione
        chiamata app.

        :param app: Nome dell'applicazione.
        :param azione: Azione che voglio eseguire.
        :return: True o False se l'utente è autorizzato o meno.
        """
        # Prendo il valore della chiave e se non la trova imposta come valore 0.
        # Faccio l'AND con l'azione richiesta e se mi viene una valore != 0 sono autorizzato altrimenti no.
        return True if self.actual_perm(app) and azione else False
    
    def actual_perm(self, app):
        """
        I permessi ATTUALI sull'app cui faccio riferimento.
        Per rispondere controlla prima se l'app è una di quelle di sistema, per cui non dipende dall'azienda, oppure no.
        :param app: Il nome dell'APP di cui voglio verificare i permessi.
        :return: I permessi attualmente posseduti su quell'app per l'azienda su cui sto operando.
        """
        real_app = app if app in self.__SYSAPP else self.azienda + '.' + app
        return self.permissions.get(real_app, 0)

    #
    # Qui iniziano i metodi con cui controllo se una certa lista di permessi 'perm' contempla quello che voglio fare con
    # l'applicazione 'app' o no.
    # Li ho scritti così perchè ho avuto problemi nella gestione dei parametri passati ai templatetags !
    #
    def can_add(self, app):
        """
        Controllo se posso aggiungere elementi.
        
        :param app: L'Applicazione su cui voglio fare il controllo.
        :return: True o False a seconda che sia autorizzato o meno.
        """
        return self.actual_perm(app) & self.OP_ADD

    def can_export(self, app):
        """
        Controllo se posso esportare elementi.

        :param app: L'Applicazione su cui voglio fare il controllo.
        :return: True o False a seconda che sia autorizzato o meno.
        """
        return self.actual_perm(app) & self.OP_EXPORT

    def can_import(self, app):
        """
        Controllo se posso importare elementi.

        :param app: L'Applicazione su cui voglio fare il controllo.
        :return: True o False a seconda che sia autorizzato o meno.
        """
        return self.actual_perm(app) & self.OP_IMPORT

    def can_read(self, app):
        """
        Controllo se posso leggere elementi.

        :param app: L'Applicazione su cui voglio fare il controllo.
        :return: True o False a seconda che sia autorizzato o meno.
        """
        return self.actual_perm(app) & self.OP_READ

    def can_update(self, app):
        """
        Controllo se posso aggiornare elementi.

        :param app: L'Applicazione su cui voglio fare il controllo.
        :return: True o False a seconda che sia autorizzato o meno.
        """
        return self.actual_perm(app) & self.OP_UPDATE

    def can_delete(self, app):
        """
        Controllo se posso cancellare elementi.

        :param app: L'Applicazione su cui voglio fare il controllo.
        :return: True o False a seconda che sia autorizzato o meno.
        """
        return self.actual_perm(app) & self.OP_DELETE
