'use strict'
var l = Ladda.create( document.querySelector( '.ladda-button' ) );

$('#tryitForm2').submit(function() {
    l.start();
    var url = 'set_new_password'; // Link til API kallet her

    $.ajax({
      type: 'POST',
      url: url,
      data: $('#tryitForm2').serialize(), // serializes the form's elements.
      success: function() {
        // 'swal' er for sweet alert.
        // Gir fin alert når serveren svarer på requesten
        swal({
          title: 'Vellykket!',
          text: 'Passordet ditt en endret',
          type: 'success',
          animation: false,
        }, function(){
            window.location.href = '/';
            });
        l.stop();
      },
      error: function() {
        l.stop();
      }
    });
    return false; // avoid to execute the actual submit of the form.
});
