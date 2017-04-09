/**
 * Created by s.pilone on 29/03/2017.
 */
$(function () {
  /* Functions */
  /* Hooks for efficiency */
  var modale = $("#modal-ordacq");

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("body").css("cursor", "progress");
      },
      success: function (data) {
        $("#modal-ordacq .modal-content").html(data.html_form);
        $("#modal-ordacq").modal("show");
        $("body").css("cursor", "default");
      }
    });
  };

  var saveForm = function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          $("#ordacq-table tbody").html(data.html_ordacq_list);
          $("#modal-ordacq").modal("hide");
        }
        else {
          $("#modal-ordacq .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };


  /* Binding */

  // Crea Ordine Acquisto
  $(".js-create-ordacq").click(loadForm);
  $("#modal-ordacq").on("submit", ".js-ordacq-create-form", saveForm);

  // Update book
  $("#ordacq-table").on("click", ".js-update-ordacq", loadForm);
  $("#modal-ordacq").on("submit", ".js-ordacq-update-form", saveForm);

  // Delete book
  $("#ordacq-table").on("click", ".js-delete-ordacq", loadForm);
  $("#modal-ordacq").on("submit", ".js-ordacq-delete-form", saveForm);

  // Import
  // Qui non aggancio l'evento al saveForm per evitare problemi con i files che altrimenti non vengono inviati
  // nell'evento POST al server.
  // $("#modal-ordacq").on("submit", ".js-ordacq-import-form", saveForm);
  // C'è un thread interessante in : http://stackoverflow.com/questions/5392344/sending-multipart-formdata-with-jquery-ajax
  $(".js-import-ordacq").click(loadForm);

});
