'use strict'
var l = Ladda.create( document.querySelector( '.ladda-button' ) );

$('#upload-form').submit(function() {
    l.start();
    var url = 'upload'; // Link til API kallet her
    var data = new FormData($('#upload-form')[0]);

    $.ajax({
      type: 'POST',
      url: url,
      data: data, //$('#upload-form').serialize(), // serializes the form's elements.
      processData: false,
      contentType: false,
      success: function() {
        // 'swal' er for sweet alert.
        // Gir fin alert når serveren svarer på requesten
        swal({
          title: 'Vellykket!',
          text: 'Endring er lagret',
          type: 'success',
          animation: false,
        }, function(){
            window.location.href = "javascript:history.back(-3)";
            });
        l.stop();
      },
      error: function() {
        l.stop();
      }
    });
    return false; // avoid to execute the actual submit of the form.
});
