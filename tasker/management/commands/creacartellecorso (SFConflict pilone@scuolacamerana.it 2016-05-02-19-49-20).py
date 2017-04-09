# coding=utf-8
from django.core.management.base import BaseCommand
from corsi.models import CartelleCorsoTask
from tasker.models import CartelleCorso
from sigutil import heartbeat, stampadebug
import time
import subprocess
import datetime

# Flag per attivare le stampe di debug
DEBUG_PRINT = False


class Command(BaseCommand):
    help = 'Crea le cartelle corso quando richiesto'

    @staticmethod
    def legge_radice():
        """
        Legge la radice delle cartelle corso dal data base di configurazione.
        La cartella radice la trovo nel DB con chiave '__RADICE__'

        :return: La radice delle cartelle corso come path completo.
        """
        dummy = CartelleCorso.objects.get(tipologia="__RADICE__")
        radice = dummy.cartelle[0]
        stampadebug("-- Cartella Radice : " + radice, DEBUG_PRINT)
        return radice

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        self.stdout.write('Cartelle Corso Lanciato !')

        while True:
            # Do un heartbeat
            self.stdout.write('-- Heartbeat : ' + str(datetime.datetime.now()))
            heartbeat(processo=CartelleCorsoTask.PROCESSO, timeout=CartelleCorsoTask.TIMEOUT)

            # Leggo la configurazione per le cartelle corso che devo preparare.
            radice = self.legge_radice()

            # Loop su tutti i task che devono essere eseguiti.
            for task in CartelleCorsoTask.objects(stato=0):
                # Stampo il corso su cui sto operando
                self.stdout.write("-- Creo Cartella per il corso : " + task.corso)

                # Come prima cosa segno che il task è in uso da me.
                task(in_uso=True, agente="CreaCartelleCorso", stato=CartelleCorsoTask.STATO_IN_LAVORAZIONE)
                task.save()

                # Adesso itero su tutte le cartelle corso che devo creare.
                dummy = CartelleCorso.objects.get(tipologia=task.tipologia)
                k = 0
                for cartella in dummy.cartelle:
                    # Creo la cartella del corso.
                    sorg = radice + "\\skel\\" + cartella
                    dest = radice + "\\" + task.anno_formativo + "\\" + task.tipologia + "\\" + task.corso + \
                        "\\" + cartella
                    flags = r'/e /o /i /y'
                    comando = "xcopy " + sorg + " " + dest + " " + flags

                    self.stdout.write("--- Comando : " + comando)
                    k += subprocess.call(comando, shell=True)

                # Aggiorno il record del task con il risultato dell'operazione.
                if k:
                    # Errore nell'operazione.
                    self.stdout.write("Errore !")
                    task(stato=CartelleCorsoTask.STATO_ERRORE, in_uso=False)
                else:
                    # Operazione andata a buon fine.
                    self.stdout.write("Tutto bene !")
                    task(stato=CartelleCorsoTask.STATO_ESEGUITO, in_uso=False)
                task.save()

            self.stdout.write("-- Sleeping for " + str(CartelleCorsoTask.LOOP) + " secondi da : " +
                              str(datetime.datetime.now()))
            time.sleep(CartelleCorsoTask.LOOP)
