# coding=utf-8
from django.core.management.base import BaseCommand
from corsi.models import CartelleCorsoTask, Corso
from tasker.models import Heartbeats
from email.mime.text import MIMEText
from sigutil import stampadebug
import time
import datetime
import smtplib


# Intervallo di riposo tra un loop e l'altro. Deve OVVIAMENTE essere minore di tutti i TIMEOUT dei vari processi
# altrimenti non è detto che me ne accorga in tempo !
LOOP = 300

# Intervallo tra le spedizioni di mail del supervisore per avvisare che è ancora vivo.
HEARTBEATS = 3*60*60

DEBUG_PRINT = False

CRLF = '\r\n'


def spedisce_mail(messaggio, subject):
    """
    Spedisce una mail con la lista degli errori

    :param messaggio: Messaggio da spedire, eventuale lista degli errori.
    :param subject: Oggetto della mail.
    :return: None.
    """
    # Compila mittente, destinatario e corpo della mail sulla base degli errori che ho riscontrato.
    sender = 'si@scuolacamerana.it'
    receiver = 'pilone@scuolacamerana.it'
    body = CRLF.join(messaggio)

    # Compone il corpo della mail secondo gli standard della posta elettronica.
    msg = MIMEText(body)
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = subject
    text = msg.as_string()

    # Avvisa dell'invio di una mail.
    print("-- Invio mail in corso...")

    # Prova a spedire la mail e segnala eventuali errori.
    try:
        smtpobj = smtplib.SMTP('mail.nethouse.it')
        smtpobj.sendmail(sender, receiver, text)
        print("-- Successfully sent email")
    except smtplib.SMTPException:
        print("-- Error: unable to send email")


def check_cartelle_corso(errori):
    """
    Controlla il task delle cartelle corso per eseguire le necessarie operazioni e per segnalare eventuali errori.

    :param errori: Lista degli eventuali errori da riportare al supervisore umano.
    :return: None
    """
    # Controllo i Task che sono andati a buon fine e marco come create le cartelle corso.
    stampadebug("-- Marcatura cartelle corso create ed ok.", DEBUG_PRINT)
    for task in CartelleCorsoTask.objects(stato=CartelleCorsoTask.STATO_ESEGUITO):
        # Stampo il corso su cui sto operando
        print("-- Registro creazione Cartella corso per : " + task.corso)

        # Recupero il corso e marco la presenza della cartella corso.
        corso = Corso.objects.get(codice_edizione=task.corso)
        corso.cartella_corso = True
        corso.save()

        # Aggiorno il task marcandolo per l'archiviazione.
        task.stato = CartelleCorsoTask.STATO_ARCHIVIARE
        task.save()

    # Verifica Task in errore per segnalazione all'amministratore
    stampadebug("-- Controllo di eventuali task in errore.", DEBUG_PRINT)
    for task in CartelleCorsoTask.objects(stato=CartelleCorsoTask.STATO_ERRORE):
        # Stampo il corso su cui sto operando ed accodo la linea d'errore.
        messaggio = "-- Task Cartelle corso con errori : " + task.corso
        print(messaggio)
        errori.append(messaggio)

        # Aggiorno lo stato del task con errore in modo che venga segnalato solo una volta.
        task.stato = CartelleCorsoTask.STATO_ATTESA_GESTIONE_ERRORE
        task.save()

    # Controlla se ci sono task in attesa di elaborazione da più di 5 minuti.
    # In questo caso vuol dire che il processo di creazione delle cartelle si è bloccato da qualche parte.
    for task in CartelleCorsoTask.objects(stato=CartelleCorsoTask.STATO_ATTESA_LAVORAZIONE):
        stampadebug("-- Controllo Skew time per  " + task.corso)
        t1 = datetime.datetime.now()
        dt = datetime.timedelta.total_seconds(t1 - task.data_aggiornamento)

        stampadebug("-- Trovato " + str(dt))
        if dt > CartelleCorsoTask.TIMEOUT:
            errori.append("Blocco dell'automa di creazione cartelle corso !!!")


def check_heartbeat(errori):
    """
    Controllo tutti gli heartbeat del data base.
    Se trovo un valore maggiore del timeout segnalo errore.

    :param errori: Lista degli eventuali errori da riportare al supervisore umano.
    :return: None
    """
    # Loop su tutti gli heartbeat
    t1 = datetime.datetime.now()
    for hb in Heartbeats.objects():
        # Leggo ultimo heartbeat
        dt = datetime.timedelta.total_seconds(t1 - hb.data_aggiornamento)
        if dt > hb.timeout:
            messaggio = "-- Blocco dell'automa : " + hb.processo
            print(messaggio)
            errori.append(messaggio)


def still_alive(last_heartbeat):
    """
    Manda un messaggio ad intervalli di HEARTBEATS per avvisare che il processo di supervisione è ancora vivo.

    :param last_heartbeat: datetime dell'ultimo avvio o dell'ultimo invio di messaggio. Il valore viene aggiornato
                            quando viene spedita una mail.
    :return: None
    """
    t1 = datetime.datetime.now()
    dt = datetime.timedelta.total_seconds(t1 - last_heartbeat)

    if dt > HEARTBEATS:
        messaggio = "-- Supervisore Sistema informatico in funzione"
        print(messaggio)
        spedisce_mail([messaggio], "Notice : Check Supervisore Sistema Informatico")
        last_heartbeat = t1
        print("-- Aggiornato Heartbeat a :" + str(last_heartbeat))


class Command(BaseCommand):
    help = 'Processo di supervisione del Sistema Informatico'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        # Segnalo avvio del supervisore.
        spedisce_mail(["Supervisore Attivato"], "Notice : Supervisore Sistema Informatico")
        lhb = datetime.datetime.now()

        while True:
            # Azzero la lista degli errori.
            errori = []

            # Verifica Cartelle corso.
            check_cartelle_corso(errori)

            # Verifica degli Heartbeat.
            check_heartbeat(errori)

            # Se ci sono stati errori spedisce una mail di richiesta di aiuto.
            if errori:
                spedisce_mail(errori, "*** ERRORE SISTEMA INFORMATICO ***")
            else:
                still_alive(lhb)

            self.stdout.write("-- Sleeping for " + str(LOOP) + " secondi da : " + str(datetime.datetime.now()))

            time.sleep(LOOP)
