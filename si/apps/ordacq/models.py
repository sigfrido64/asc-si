# coding=utf-8
from django.db import models
from django.core.validators import MinLengthValidator

# Create your models here.


class TabellaStatoOrdini(models.Model):
    """
    Definizione della tabella stato ordini che mi serve per la visione d'insieme.
    Questa tabella, in futuro potrebbe anche sparire in quanto sostituita da query su ordini e su altre
    tabelle.
    """
    # Qui definisco gli stati in modo che siano poi semplici da gestire.
    STATO_BOZZA = 1
    STATO_EMETTERE = 2
    STATO_FIRMATO = 3
    STATO_SPEDITO = 4
    STATO_CHOICES = (
        (STATO_BOZZA, 'Bozza'),
        (STATO_EMETTERE, 'Emettere'),
        (STATO_FIRMATO, 'Firmato'),
        (STATO_SPEDITO, 'Spedito')
    )

    TIPO_ACQ = 1
    TIPO_ABB = 2
    TIPO_CHOICES = (
        (TIPO_ACQ, 'Acquisto'),
        (TIPO_ABB, 'Abbonamento')
    )

    azienda = models.CharField(max_length=10, default="ASC")
    anno = models.CharField(max_length=10, default="2016/2017")
    # Il protocollo è il numero di protocollo dell'ordine, se presente. Posso avere più righe della tabella stato
    # ordini che fanno riferimento allo stesso ordine solo se in mesi differenti.
    protocollo = models.CharField(
        # Dovrebbe essere nella forma standard Camerana.
        max_length=6,
        validators=[MinLengthValidator(3)], verbose_name="Numero di protocollo dell'ordine se presente", blank=True)
    # Contratto è il riferimento al contratto, se esiste.
    contratto = models.CharField(
        max_length=80,
        verbose_name="Riferimento al contratto con il fornitore, se presente.", blank=True)
    data = models.DateField(
        verbose_name="Data dell'ordine")
    competenza = models.CharField(
        max_length=10,
        verbose_name="Mese di competenza dell'ordine, nel caso di più mesi devo inserire più righe")
    stato = models.IntegerField(choices=STATO_CHOICES, default=STATO_BOZZA)
    fornitore = models.CharField(
        max_length=80, verbose_name="Nome del fornitore")
    tipo = models.IntegerField(choices=TIPO_CHOICES, default=TIPO_ACQ)
    descrizione = models.CharField(max_length=120, verbose_name="Descrizione dell'ordine")
    iniziativa = models.CharField(max_length=80, verbose_name="Iniziativa/e di riferimento")
    imponibile = models.IntegerField(verbose_name="Imponibile dell'ordine")
    iva_presente = models.BooleanField(default=True, verbose_name="Mi dice se l'IVA è presente")
    iva_detraibile = models.IntegerField(verbose_name="Percentuale di IVA detraibile")
    totale_costo = models.IntegerField(verbose_name="Costo totale dell'ordine comprensivo di IVA indetraibile")
    pagamento = models.CharField(
        max_length=80,
        verbose_name="scadenza di pagamento dell'ordine")
    fatture_protocolli = models.CharField(
        max_length=80,
        verbose_name="Numero/i di protocollo delle fatture")
    note = models.CharField(
        max_length=1000,
        verbose_name="Eventuali note sull'ordine")

    in_uso = models.BooleanField(db_index=True, default=True, verbose_name="L'ordine è valido ?")

    # Date di creazione e di aggiornamento dell'elemento.
    data_aggiornamento = models.DateTimeField(auto_now=True)
    data_creazione = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.fornitore + ' - ' + self.descrizione + ' - ' + self.protocollo

    def save(self, *args, **kwargs):
        if self.iva_presente:
            self.totale_costo = self.imponibile * 1.22 * (100 - self.iva_detraibile) / 100
        super(TabellaStatoOrdini, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Ordine"
        verbose_name_plural = "Ordini"

