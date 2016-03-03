var options = {
  valueNames: [ 'name', 'description', 'name1', 'description1' ]
};
var projectList = new List('projects', options);

$(document).ready(function(){
    $('.prosjekt-child').click(function(){
        $(this).children().slideToggle();
    });

});

function submit(id) {
     document.getElementById(id).submit();
}


var divs = $('div[data-filter]');
$('#search').on('keyup', function() {
    var val = $.trim(this.value);
    divs.hide();
    divs.filter(function() {
        return $(this).data('filter').search(val.ignoreCase) >= 0
    }).show();

    if ($(this).val() == "") {
        $(".el").hide();
            }
});
