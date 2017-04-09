# coding=utf-8

from django.forms.widgets import Widget
from django.utils.html import format_html
from django.forms.utils import flatatt
from django.utils.encoding import force_text
import json
import dateutil.parser as data_parser
from globvar import js_append


# Compone la parte iniziale del Document Ready (Document Ready Head)
DRH_STRING = '<script type="text/javascript">$(document).ready(function () {'
# Compone la parte finale del Document Ready (Document Ready Tail)
DRT_STRING = '});</script>'

# Dizionario con i nomi dei controlli per semplificare il lookup


def _selettore(name):
    """
    Crea il Javascript per lo specifico selettore.
    :param name: Nome del selettore.
    """
    return '$("#' + name + '")'


def _to_jsdate(data):
    """
    Converte una data nel formato nostro GG/MM/YYYY in YYYY-MM-DD per renderla compatibile con il Javascript

    :param data: La data da convertire.
    :return: Una stringa con la data convertita.
    """
    dt = data_parser.parse(data, dayfirst=True)
    return str(dt)


def _flatjqxatt(jqwattrs, extra_args=None, prologo='({ ', epilogo='});'):
    """
    Converte un dizionario di attributi in una stringa.
    Ritorno 'prologo' seguito da coppie nome: valore e con terminale 'epilogo'
    I numeri vengono scritti come numeri e le stringhe comprese tra apici ('). Per le parole riservate di Javascript
    e per i valori degli array di parametri uso la convenzione che se la stringa inizia con hash (#) verrà scritta
    senza apici (') e togliendole l'hash (#) iniziale.
    Il risultato non passa da html_safe perchè essendo un javascript mi taglierebbe il codice.

    :param jqwattrs: Dizionario da tradurre
    :param extra_args: Stringa che verrà messa dentro la traduzione esattamente così com'è !! OKKIO !!
    :param prologo: Stringa da mettere all'inizio.
    :param epilogo: Stringa da mettere alla fine.
    """
    # return '({ ' + ', '.join([": ".join([key, str(val)]) for key, val in jqwattrs.items()]) + '});'
    # Se ho degli extra_args gli aggiungo una ', ' per rendere consistente l'output.
    if extra_args is None:
        extra_args = ''
    else:
        extra_args += ', '
    # Qui invece converto il dizionario.
    linea = ''
    for key, val in jqwattrs.items():
        if type(val) is str:
            if val[0] == '#':
                # Se è una keyword (inizia con hash (#)) la metto tal quale.
                kw = key + ': ' + val[1:]
            else:
                # Altrimenti la metto tra apici ed usando json mi assicuro anche un corretto escaping delle stringhe !
                kw = key + ": " + json.dumps(val)
        elif type(val) is bool:
            # Ricorro a json dumps perchè il True ed il False in Jscript si scrivono in minuscolo !!!
            kw = key + ": " + json.dumps(val)
        else:
            # Altrimenti la mando in uscita così com'è.
            kw = key + ": " + str(val)
        # Metto le virgole tra un elemento e l'altro.
        if linea == '':
            linea = kw
        else:
            linea += ', ' + kw
    return prologo + extra_args + linea + epilogo


def _datafieldsgenerator(datafields):
    pass


def _check_necessari(lista, must, controllo=''):
    """
    Controlla se ci sono tutti gli elementi dichiarati come necessari ('must') e che non possono avere un valore di
    default in quanto sono quelli caratterizzanti.

    :param lista: Dizionario da controllare.
    :param must: Lista degli elementi che devono comparire nelle chiavi.
    :param controllo : Nome del controllo su cui opero. Serve solo per avere un errore parlante in caso lo debba
        segnalare.
    :return: None
    """
    # Controllo che ci siano tutti i valori necessari.
    for chiave in must:
        if chiave not in lista.keys():
            raise NotImplementedError("{0} deve essere definito quando dichiaro {1} !!!!".format(chiave, controllo))
    return


def _check_datagridcolumns(campo):
    """
    Controlla che il 'campo' che passo come parametro e che definisce le columns del controllo DataGrid contenga
    almeno il nome ed il campo da cui prendere il valore. Gli altri campi sono opzionali !

    :param campo: Lista delle columns che voglio controllare.
    :return: None. In caso manchino i paramentri minimi necessari solleva eccezione !
    """
    must = ['text', 'dataField']
    for riga in campo:
        for chiave in must:
            if chiave not in riga.keys():
                raise NotImplementedError("Per i datagrid bisogna definire 'text' e 'dataField' in ogni 'columns' !!")


def _data_adapter(jqxattrs):
    """
    Compone il controllo di tipo JqxDataAdapter in funzione della lista di parametri che trova in ingresso.

    :param jqxattrs: Il dizionario con i parametri che passo alla funzione JqxDataGrid. Per cui necessita di un
        'ritocchino' !
    :return: La stringa da mettere direttamente nel codice. La stringa non subisce escapes di nessun tipo in quanto
        produrrebbe un output monco !
    """
    # Come prima cosa prendo il valore di 'url' e lo metto nel dizionario specifico del DataAdapter.
    jqxda = dict()
    jqxda['url'] = jqxattrs['url']

    # Estraggo i datafields dalla definizione delle colonne del DataGrid.
    # Attenzione all'hash (#) iniziale che metto solo affinchè in uscita la voce datafields venga mandata senza ".
    lista = jqxattrs['columns']
    datafields = "#[{ name: 'pk' },"
    for elemento in lista:
        datafields += "{{ name: '{0}' }},".format(elemento['dataField'])
    datafields += ']'
    jqxda['datafields'] = datafields

    # Setto i defaults.
    default = {'datatype': 'json', 'id': 'pk'}
    jqxda.update(default)

    # Compone la parte del source del data adapter
    # Riporta il codice e trattandosi di JqxDataAdapter mette prologo ed epilogo specifici.
    source = _flatjqxatt(jqxda, prologo='var source = {', epilogo='};')

    # Compone la parte specifica del Data Adpter.
    da = 'var dataAdapter = new $.jqx.dataAdapter(source);'
    return source + da


class JqxWidget(Widget):
    """
    Classe generale per la gestione dei Widgets Jqx.
    """
    def __init__(self, attrs=None, jqwattrs=None):
        # Setto i valori di default a seconda del tipo.
        self.jqwattrs = dict()
        if type(self) is JqxInput:
            # Se di tipo JqxInput setto altezza di default.
            self.jqwattrs = dict(height=25)
        elif type(self) is JqxDateTimeInput:
            # Invece per la data metto di default la nostra rappresentazione DD-MM-YYYY
            self.jqwattrs = dict(culture='it-IT')
        elif type(self) is JqxDataGrid:
            # Per i default setto quelli che sono diversi dai default di JqWidgets.
            self.jqwattrs = dict(columnsresize=True, autoheight=True, autorowheight=True, pageable=True, pagesize=20,
                                 filterable=True, sortable=True, source='#dataAdapter')

        # Se ci sono altri elementi da aggiungere li aggiunge.
        if jqwattrs is not None:
            self.jqwattrs.update(jqwattrs)
        super(JqxWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        """
        Returns this Widget rendered as HTML, as a Unicode string.

        The 'value' given is not guaranteed to be valid input, so subclass
        implementations should program defensively.
        :param attrs:
        :param value:
        :param name:
        """
        raise NotImplementedError('subclasses of Widget must provide a render() method')

    def build_jqwattrs(self, extra_attrs=None, **kwargs):
        """
        Helper function for building an attribute dictionary.
        :param extra_attrs: Dizionario con altri parametri.
        :param kwargs: Serie di parametri nella forma chiave = valore come per i dizionari.
        :return:
        """
        jqwattrs = dict(self.jqwattrs, **kwargs)
        if extra_attrs:
            jqwattrs.update(extra_attrs)
        return jqwattrs


class JqxInput(JqxWidget):
    """
    Interfaccia per il controllo JqxInput

    I Valori di default sono nella classe madre JqxWidget.
    """
    def render(self, name, value, attrs=None, jqwattrs=None):
        # Aggiunte specifiche per il controllo per la parte HTML.
        final_attrs = self.build_attrs(attrs, type='text', name=name)

        # Only add the 'value' attribute if a value is non-empty.
        if value is not None:
            final_attrs['value'] = force_text(value)

        # Parte Jqw
        final_jqwattrs = self.build_jqwattrs(jqwattrs)

        # Compone il javascript specifico. Non faccio escapes in quanto me li intercetterebbe.
        id_name = final_attrs['id']
        js = _selettore(id_name) + '.jqxInput' + _flatjqxatt(final_jqwattrs)
        js = DRH_STRING + js + DRT_STRING
        # E gli faccio seguire l'html specifico del controllo secondo JqWidgets.
        html = js + format_html('<input{} />', flatatt(final_attrs))
        return html


class JqxDateTimeInput(JqxWidget):
    """
    Interfaccia per il controllo JqxDateTimeInput

    I Valori di default sono nella classe madre JqxWidget.
    """
    def render(self, name, value, attrs=None, jqwattrs=None):
        # Aggiunte specifiche per il controllo per la parte HTML.
        final_attrs = self.build_attrs(attrs, name=name)

        # Parte Jqw
        final_jqwattrs = self.build_jqwattrs(jqwattrs)
        if value is not None:
            # Only add the 'value' attribute if a value is non-empty.
            final_jqwattrs['value'] = _to_jsdate(value)

        # Compone il javascript specifico. Non faccio escapes in quanto me li intercetterebbe.
        id_name = final_attrs['id']
        js = _selettore(id_name) + '.jqxDateTimeInput' + _flatjqxatt(final_jqwattrs)
        js = DRH_STRING + js + DRT_STRING
        # E gli faccio seguire l'html specifico del controllo secondo JqWidgets.
        html = js + format_html('<div{}> </div>', flatatt(final_attrs))
        return html


class JqxTextArea(JqxWidget):
    """
    Interfaccia per il controllo JqxTextArea

    I Valori di default sono nella classe madre JqxWidget.
    """
    def render(self, name, value, attrs=None, jqwattrs=None):
        # Aggiunte specifiche per il controllo per la parte HTML.
        final_attrs = self.build_attrs(attrs, name=name)

        # Parte Jqw
        final_jqwattrs = self.build_jqwattrs(jqwattrs)

        # Se il controllo ha un valore iniziale lo metto nella variabile che obbligatoriamente devo usare per
        # passare il valore iniziale al controllo.
        id_name = final_attrs['id']
        js1 = ''
        if value is not None:
            # Only add the 'value' attribute if a value is non-empty.
            js1 = _selettore(id_name) + ".jqxTextArea ('val', " + json.dumps(value) + ");"

        # Compone il javascript specifico. Non faccio escapes in quanto me li intercetterebbe.
        js = _selettore(id_name) + '.jqxTextArea' + _flatjqxatt(final_jqwattrs)
        js = DRH_STRING + js + js1 + DRT_STRING
        # E gli faccio seguire l'html specifico del controllo secondo JqWidgets.
        html = js + format_html('<textarea {}> </textarea>', flatatt(final_attrs))
        return html


class JqxComboBox(JqxWidget):
    """
    Interfaccia per il controllo JqxComboBox

    I Valori di default sono nella classe madre JqxWidget.
    """
    def render(self, name, value, attrs=None, jqwattrs=None):
        # Aggiunte specifiche per il controllo per la parte HTML.
        final_attrs = self.build_attrs(attrs, name=name)

        # Parte Jqw
        final_jqwattrs = self.build_jqwattrs(jqwattrs)

        # Se il controllo ha un valore iniziale lo metto nella variabile che obbligatoriamente devo usare per
        # passare il valore iniziale al controllo.
        id_name = final_attrs['id']
        js1 = ''
        if value is not None:
            # Only add the 'value' attribute if a value is non-empty.
            js1 = _selettore(id_name) + ".jqxComboBox ('val', " + json.dumps(value) + ");"

        # Compone il javascript specifico. Non faccio escapes in quanto me li intercetterebbe.
        js = _selettore(id_name) + '.jqxComboBox' + _flatjqxatt(final_jqwattrs)
        js = DRH_STRING + js + js1 + DRT_STRING
        # E gli faccio seguire l'html specifico del controllo secondo JqWidgets.
        html = js + format_html('<div{}> </div>', flatatt(final_attrs))
        return html


class JqxDataAdapter(JqxWidget):
    """
    Interfaccia per il controllo JqxDataAdapter. Essendo un controllo interno non si rifà a Widget
    """
    def render(self, name, value, attrs=None, jqwattrs=None):
        # print(_data_adapter({'url': '/si/corsi/api/get_corsi/',
        # 'datafields': ('data', 'inizio', 'fine', 'sede', 'pk')}))
        # Aggiunte specifiche per il controllo per la parte HTML.
        # final_attrs = self.build_attrs(attrs, name=name)
        final_attrs = self.build_attrs(attrs)

        # Parte Jqw
        final_jqwattrs = self.build_jqwattrs(jqwattrs)

        # Se il controllo ha un valore iniziale lo metto nella variabile che obbligatoriamente devo usare per
        # passare il valore iniziale al controllo.
        id_name = final_attrs['id']
        js1 = ''
        if value is not None:
            # Only add the 'value' attribute if a value is non-empty.
            js1 = self.selettore(id_name) + ".jqxComboBox ('val', " + json.dumps(value) + ");"

        # Compone il javascript specifico. Non faccio escapes in quanto me li intercetterebbe.
        js = _selettore(id_name) + '.jqxComboBox' + _flatjqxatt(final_jqwattrs)
        js = DRH_STRING + js + js1 + DRT_STRING
        # E gli faccio seguire l'html specifico del controllo secondo JqWidgets.
        html = js + format_html('<div{}> </div>', flatatt(final_attrs))
        return html


class JqxDataGrid(JqxWidget):
    """
    Interfaccia per il controllo JqxDataGrid

    La chiave primaria da usare nelle varie interfacce è pk !
    I Valori di default sono nella classe madre JqxWidget.
    """
    def render(self, name, value, attrs=None, jqwattrs=None):
        # Compongo i dizionari per la parte HTML e per la parte Jqwidgets.
        final_attrs = self.build_attrs(attrs, name=name)
        final_jqwattrs = self.build_jqwattrs(jqwattrs)

        # Come must ho bisogno almeno dell'url da interrogare e delle colonne da mostrare.
        must = ('url', 'columns')
        _check_necessari(final_jqwattrs, must=must, controllo='JqxDataGrid')

        # Ora devo controllare che il campo colums che c'è, perchè ho già controllato che esiste, contenga gli
        # elementi minimi necessari.
        _check_datagridcolumns(campo=final_jqwattrs['columns'])

        # Se arrivo qui i campi minimi ci sono tutti ed i default sono ok !
        # Preparo quindi il DataAdapter di partenza !
        da = _data_adapter(final_jqwattrs)

        # Elimino da jqwattrs gli elementi specifici del Data Adapter.
        del final_jqwattrs['url']

        # Setto il nome del controllo in funzione del nome del campo.
        id_name = final_attrs['id']

        # Compone il javascript specifico. Non faccio escapes in quanto me li intercetterebbe.
        js = _selettore(id_name) + '.jqxGrid' + _flatjqxatt(final_jqwattrs)
        
        # Compongo i jsvascript specifici sia per il data adapter che per la griglia.
        js = DRH_STRING + da + js + DRT_STRING
                
        # Html specifico del controllo secondo JqWidgets e gli metto in coda i javascript
        html = format_html('<div{}> </div>', flatatt(final_attrs)) + '\n' + js
        
        return html

"""
            var url = "/si/corsi/api/get_corsi/";
            var grid = $("#jqxgrid");
            // prepare the data
            var source = {
                datatype: "json",
                datafields: [
                    { name: 'data' },
                    { name: 'inizio' },
                    { name: 'fine' },
                    { name: 'sede' },
                    { name: 'pk' }
                ],
                id: 'pk',
                url: url,
                root: 'data',
                data: {
                    style: "full",
                    maxRows: 50
                }
            };
            var dataAdapter = new $.jqx.dataAdapter(source, {
                formatData: function (data) {
                    $.extend(data, {
                        filtroCorso: $('#filtroCorso').val(),
                        style: "full",
                        maxRows: 50
                    });
                return data;
                }
            });

"""

"""
            grid.jqxGrid({
                width: "100%",
                source: dataAdapter,
                // DONE columnsresize: true,
                // DEFAULT ! editable: false,
                // DONE autoheight: true,
                // DONE autorowheight: true,
                // DONE pageable: true,
                // DONE pagesize: 20,
                // DONE filterable: true,
                // DONE sortable: true,
                // DEFAULT autoshowfiltericon: true,
                columns: [
                    { text: 'Codice Corso', dataField: 'codice', width: "10%" },
                    { text: 'Denominazione', dataField: 'denominazione', width: "70%" },
                    { text: 'Durata', dataField: 'durata', width: "10%" },
                    { text: 'Ordine', dataField: 'ordine', width: "10%" }
                ],
                showstatusbar: true,
                renderstatusbar: function (statusbar) {
                    // appends buttons to the status bar.
                    var container = $("<div style='overflow: hidden; position: relative; margin: 5px;'></div>");
                    var addButton = $("<div style='float: left; margin-left: 5px;'><img style='position: relative;
                        margin-top: 2px;' src='{% static "jqw/images/add.png" %}'/><span style='margin-left: 4px;
                        position: relative; top: -3px;'>Add</span></div>");
                    var deleteButton = $("<div style='float: left; margin-left: 5px;'><img style='position: relative;
                        margin-top: 2px;' src='{% static "jqw/images/close.png" %}'/><span style='margin-left: 4px;
                        position: relative; top: -3px;'>Delete</span></div>");
                    var reloadButton = $("<div style='float: left; margin-left: 5px;'><img style='position: relative;
                        margin-top: 2px;' src='{% static "jqw/images/refresh.png" %}'/><span style='margin-left: 4px;
                        position: relative; top: -3px;'>Reload</span></div>");
                    var searchButton = $("<div style='float: left; margin-left: 5px;'><img style='position: relative;
                        margin-top: 2px;' src='{% static "jqw/images/search.png" %}'/><span style='margin-left: 4px;
                        position: relative; top: -3px;'>Find</span></div>");
                    container.append(addButton);
                    container.append(deleteButton);
                    container.append(reloadButton);
                    container.append(searchButton);
                    statusbar.append(container);
                    addButton.jqxButton({  width: 65, height: 20 });
                    deleteButton.jqxButton({  width: 65, height: 20 });
                    reloadButton.jqxButton({  width: 65, height: 20 });
                    searchButton.jqxButton({  width: 50, height: 20 });
                    // add new row.
                    addButton.click(function (event) {
                        window.location.href = "{% url 'corsi:add' %}";
                        var datarow = generatedata(1);
                        $("#jqxgrid").jqxGrid('addrow', null, datarow[0]);
                    });
                    // delete selected row.
                    deleteButton.click(function (event) {
                        var selectedrowindex = $("#jqxgrid").jqxGrid('getselectedrowindex');
                        var rowscount = $("#jqxgrid").jqxGrid('getdatainformation').rowscount;
                        var id = $("#jqxgrid").jqxGrid('getrowid', selectedrowindex);
                        $("#jqxgrid").jqxGrid('deleterow', id);
                    });
                    // reload grid data.
                    reloadButton.click(function (event) {
                        $("#jqxgrid").jqxGrid({ source: getAdapter() });
                    });
                    // search for a record.
                    searchButton.click(function (event) {
                        var offset = $("#jqxgrid").offset();
                        $("#jqxwindow").jqxWindow('open');
                        $("#jqxwindow").jqxWindow('move', offset.left + 30, offset.top + 30);
                    });
                },
            });
"""
