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



