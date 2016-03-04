var options = {
  valueNames: [ 'name', 'description', 'comment', 'desc', 'user']
};
var projectList = new List('projects', options);


/*
var divs = $('tr[data-filter]');

$('#search').on('keyup', function() {
    divs.hide();

    var val = $.trim(this.value);
    divs.filter(function() {


        //var a = $(this).data('filter');
        //a = a.search(val.ignoreCase);
        //a = a >= 0;
        //return $(this).data('filter').search(val.ignoreCase) >= 0
    }).show();


    if ($(this).val() == "") {
        divs.show();
            }
});*/
