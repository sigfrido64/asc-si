@register.simple_tag()
def si_dc_dialog():
    tag = """
    <script>
    $(function() {
        $(".remove_link").click(function(e) {
        e.preventDefault();     // Previene l'apertura dell'url di cancellazione.
        var url = $(this).attr("link");     // Compone le variabili per il dialog.
        var item = $(this).attr("item");
        var title = $(this).attr("titolo");
        var testo = "Attenzione !!!<br><strong><div align='center'>" + item + "</div></strong><br> verrà cancellato in modo permanente !!";

        $("#dialog").html(testo);
        $("#dialog").dialog({
                title: title,
                closed: false,
                modal: true,
                width: 450,
                height: 200,

                close: function(event, ui) {$("#dialog").empty();},   // Rimuove il contenuto.
                buttons: [{
                    text:'Elimina',
                    iconCls:'icon-no',
                    handler:function(){
                        window.location.href = url;
                        $("#dialog").dialog("close");
                    }
                },{
                    text:'Annulla',
                    iconCls:'icon-back',
                    handler:function(){
                        $("#dialog").dialog("close");
                    }
                }]
                //END CLOSE
            });//END DIALOG
        $("#dialog").dialog("open");
        });//END DIALOG
    });//END MODAL_LINK
//END FUNCTION
</script>
    <div id="dialog" class="easyui-dialog" title="Conferma Cancellazione" style="width:400px;height:200px;padding:10px" data-options="iconCls:'icon-no',modal:true,closed:true">
        The dialog content.
    </div>
"""
    return mark_safe(tag)


# Vecchia versione
"""
    <div id="dialog" title="Basic dialog">
    </div>

    <script>
    $(function() {
        $(".remove_link").click(function(e) {
        e.preventDefault();     // Previene l'apertura dell'url di cancellazione.
        var url = $(this).attr("link");     // Compone le variabili per il dialog.
        var item = $(this).attr("item");
        var title = $(this).attr("titolo");
        var testo = "Attenzione !!!<br><strong><div align='center'>" + item + "</div></strong><br> verrà cancellato in modo permanente !!";

        $("#dialog").html(testo);
        $("#dialog").dialog({
                title: title,
                modal: true,
                width: 450,
                close: function(event, ui) {$("#dialog").empty();},   // Rimuove il contenuto.
                show: {
                    effect: "explode",
                    duration: 1000,
                    distance: 500
                },
                hide: {
                    effect: "explode",
                    duration: 1000
                },
                buttons: {
                    "Annulla": function() {
                        $( this ).dialog( "close" );
                    },
                    "Elimina": function() {
                    window.location.href = url;
                    $(this).dialog( "close" );
                    }
                }

                //END CLOSE
            });//END DIALOG
        $("#dialog").dialog("open");
        });//END DIALOG
    });//END MODAL_LINK
//END FUNCTION
</script>
"""


