/**
 * Created by Sig on 09/02/2017.
 */
$(document).ready(function () {
    var source = {
        id: "pk",
        datatype: "json",
        url: "/si/iniziative/api/get_iniziative/",
        datafields: [{ name: 'pk' },
                     { name: 'nome' },
                     { name: 'descrizione' },
        ]};
    var dataAdapter = new $.jqx.dataAdapter(source);
    $("#id_your_name").jqxGrid({
        autoheight: true,
        source: dataAdapter,
        sortable: true,
        columnsresize: true,
        autorowheight: true,
        columns: [
            {'dataField': 'nome', 'width': '20%', 'text': 'Nome'},
            {'dataField': 'descrizione', 'width': '80%', 'text': 'Descrizione'}
        ],
        width: "100%",
        filterable: true,
        pagesize: 20,
        pageable: true
    });
});