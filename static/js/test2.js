'use strict'
var l = Ladda.create( document.querySelector( '.ladda-button' ) );

$('#tryitForm2').submit(function() {
    l.start();
});