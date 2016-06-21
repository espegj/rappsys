$("document").ready(function () {

    var postPage = $("#postPage").hide();
    var dataPage = $("#data").show();
    var data2Page = $("#data2").show();
    var backButton = $("#back").hide();
    var logOut = $("#logOut");
    var parent;

    var element;
    function findElement(source, id, isFolder, isActivity)
        {
            var t = 0;
            for (key in source)
            {
                var item = source[key];
                if(item[0]){
                    if(item[0].isFolder || item[0].isActivity){
                        if(item[0].id==id && item[0].isFolder==isFolder && item[0].isActivity==isActivity)
                            element = item[0];
                    }
                }
                else{
                    if(item.isFolder || item.isActivity){
                        if(item.id==id && item.isFolder==isFolder && item.isActivity==isActivity)
                            element = item;
                    }
                }
                if (item[1])
                {
                    findElement(item[1], id, isFolder, isActivity);
                }
                else{
                    findElement(item.nodes, id, isFolder, isActivity);
                }
            }
        }


    var parent;
    var parentList=[];
    var check = false;
    function getProject(source, id, isFolder, isActivity)
        {
            for (key in source)
            {
                if (check){
                    parent = parentList[parentList.length - 1];
                    alert(parent.text);
                }


                check=false;
                var item = source[key];
                if(item[0]){
                    if(item[0].isFolder || item[0].isActivity){
                        if(item[0].id==id && item[0].isFolder==isFolder && item[0].isActivity==isActivity){
                            check=true;
                            }
                    }
                }
                else{
                    if(item.isFolder || item.isActivity){
                        if(item.id==id && item.isFolder==isFolder && item.isActivity==isActivity){
                            check=true;
                            }
                    }
                }
                if (item[1])
                {
                    parentList.push(item[0]);
                    getProject(item[1], id, isFolder, isActivity);
                }
                else{
                    getProject(item.nodes, id, isFolder, isActivity);
                }
            }
        }

    function findColor(data){
        if(data.isFolder)
            return "green";

        else if(data.isActivity)
            return "red";

        else
            return "blue";
    }

    var data = $.parseJSON($.ajax({
        url:  'getJson',
        dataType: "json",
        async: false
    }).responseText);

    var items = data.nodes.map(function (item) {
            return [item, item.nodes];
        });

    function listAll(data)
        {
            for (key in data)
            {
                var item = data[key];

                if(item[0]){
                    if(item[0].isFolder || item[0].isActivity){
                        $( "#data" ).append( "<div class='test "+findColor(item[0])+" list-group-item li el el2' id='"+item[0].id+"' onclick=getNodes("+item[0].id+","+item[0].isFolder+","+item[0].isActivity+");>"
                            +"<div class='row'>"
                            +"<div class='col-xs-2 inner'><h1 class='white text-center'><i class='fa fa-folder'></i></h1>"
                            +"</div>"
                            +"<div class='col-xs-9'><h4 class='white name1'>"+item[0].text+"</h4></div>"
                            +"<div class='col-xs-8 col-md-4'>"
                            + "   <hr>"
                            +"<div class='col-xs-12'><p class='white name1'>"+item[0].description+"</p></div>"
                            +"</div>"
                            +"</div>"
                            +"</div>"
                        +"</div>" );
                    }
                }
                else{
                    if(item.isFolder || item.isActivity){
                        $( "#data" ).append( "<div class='test "+findColor(item)+" list-group-item li el el2' id='"+item.id+"' onclick=getNodes("+item.id+","+item.isFolder+","+item.isActivity+");>"
                            +"<div class='row'>"
                            +"<div class='col-xs-2 inner'><h1 class='white text-center'><i class='fa fa-folder'></i></h1>"
                            +"</div>"
                            +"<div class='col-xs-9'><h4 class='white name1'>"+item.text+"</h4></div>"
                            +"<div class='col-xs-8 col-md-4'>"
                            + "   <hr>"
                            +"<div class='col-xs-12'><p class='white name1'>"+item.description+"</p></div>"
                            +"</div>"
                            +"</div>"
                            +"</div>"
                        +"</div>" );
                    }
                }
                if (item[1])
                {
                    listAll(item[1]);
                }
                else{
                    listAll(item.nodes);
                }
            }
        }


    $.each( data.nodes, function( val ) {
            $( "#data" ).append( "<div class='test blue list-group-item li el el3' id='"+data.nodes[val].id+"' onclick=getNodes("+data.nodes[val].id+","+data.nodes[val].isFolder+","+data.nodes[val].isActivity+");>"
                            +"<div class='row'>"
                            +"<div class='col-xs-2 inner'><h1 class='white text-center'><i class='fa fa-folder'></i></h1>"
                            +"</div>"
                            +"<div class='col-xs-9'><h4 class='white name1'>"+data.nodes[val].text+"</h4></div>"
                            +"<div class='col-xs-8 col-md-4'>"
                            + "   <hr>"
                            +"<div class='col-xs-12'><p class='white name1'>"+data.nodes[val].description+"</p></div>"
                            +"</div>"
                            +"</div>"
                        +"</div>"
                    +"</div>" );
    });


    getNodes = function getNodes(id, isFolder, isActivity, back){
        $("#data2").empty().show();
        dataPage.hide();
        backButton.show();
        logOut.hide();
        if(parent==="project" && back==1){
            $('.el').show();
            $('.el2').hide();
            home();
        }
        parent = getParent(id,isFolder,isActivity);
        postPage.hide();
        postPage.hide();
        $("#search").show();
        $('#search').val('');
        $("#back").attr('onclick', 'getNodes('+parent.id+','+parent.isFolder+','+parent.isActivity+',1)');
        if (isActivity){
            postPage.show();
            data2Page.hide();
            dataPage.hide();
            findElement(items, id, isFolder, isActivity);
            $("#postPage h2").html(element.text);
            $("#postPage p").html(element.description);
            $("#activityInput").val(element.id);
            $("#search").hide();
        }


        function find(source, id, isFolder, isActivity)
        {
            for (key in source)
            {
                var item = source[key];
                if (item.id == id && item.isFolder == isFolder && item.isActivity == isActivity){
                    return item;
                }

                if (item.nodes)
                {
                    var subresult = find(item.nodes, id, isFolder, isActivity);
                    if (subresult)
                        return subresult;
                }
            }
            return null;
        }
        for (key in items)
        {
            var item = items[key];
            if (item[0].id == id && item[0].isFolder == isFolder && item[0].isActivity == isActivity){
                if(item[0].nodes){
                    for (i in item[0].nodes){
                        $( "#data2" ).append( "<div class='test "+findColor(item[0].nodes[i])+" list-group-item li' id='"+item[0].nodes[i].id+"' onclick=getNodes("+item[0].nodes[i].id+","+item[0].nodes[i].isFolder+","+item[0].nodes[i].isActivity+");>"
                            +"<div class='row'>"
                            +"<div class='col-xs-2 inner'><h1 class='white text-center'><i class='fa fa-folder'></i></h1>"
                            +"</div>"
                            +"<div class='col-xs-9'><h4 class='white name1'>"+item[0].nodes[i].text+"</h4></div>"
                            +"<div class='col-xs-8 col-md-4'>"
                            + "   <hr>"
                            +"<div class='col-xs-12'><p class='white name1'>"+item[0].nodes[i].description+"</p></div>"
                            +"</div>"
                            +"</div>"
                        +"</div>"
                    +"</div>" );
                    }
                }
                else{
                    $( "#data2" ).append( "<div class='test "+findColor(item[0])+" list-group-item li' id='"+item[0].id+"' onclick=getNodes("+item[0].id+","+item[0].isFolder+","+item[0].isActivity+");>"
                            +"<div class='row'>"
                            +"<div class='col-xs-2 inner'><h1 class='white text-center'><i class='fa fa-folder'></i></h1>"
                            +"</div>"
                            +"<div class='col-xs-9'><h4 class='white name1'>"+item[0].text+"</h4></div>"
                            +"<div class='col-xs-8 col-md-4'>"
                            + "   <hr>"
                            +"<div class='col-xs-12'><p class='white name1'>"+item[0].description+"</p></div>"
                            +"</div>"
                            +"</div>"
                        +"</div>"
                    +"</div>" );
                }
            }
            if (item[0].nodes){
                var subresult = find(item[0].nodes, id, isFolder, isActivity);
                if (subresult){
                    if(subresult.nodes){
                        for (i in subresult.nodes){
                            $( "#data2" ).append( "<div class='test "+findColor(subresult.nodes[i])+" list-group-item li' id='"+subresult.nodes[i].id+"' onclick=getNodes("+subresult.nodes[i].id+","+subresult.nodes[i].isFolder+","+subresult.nodes[i].isActivity+");>"
                            +"<div class='row'>"
                            +"<div class='col-xs-2 inner'><h1 class='white text-center'><i class='fa fa-folder'></i></h1>"
                            +"</div>"
                            +"<div class='col-xs-9'><h4 class='white name1'>"+subresult.nodes[i].text+"</h4></div>"
                            +"<div class='col-xs-8 col-md-4'>"
                            + "   <hr>"
                            +"<div class='col-xs-12'><p class='white name1'>"+subresult.nodes[i].description+"</p></div>"
                            +"</div>"
                            +"</div>"
                        +"</div>"
                    +"</div>" );
                        }
                    }

                }

            }
        }
    }

    $.expr[':'].containsIgnoreCase = function (n, i, m) {
            return jQuery(n).text().toUpperCase().indexOf(m[3].toUpperCase()) >= 0;
        };

    listAll(items);
    var el2 = $(".el2").hide();
    var divs = $('.el');
        $('#search').on('keyup', function() {
            var val = $.trim(this.value);
            divs.hide();
            data2Page.show();
            dataPage.show();
            postPage.hide();
            $( ".el:containsIgnoreCase('"+val+"')" ).show();
            if ($(this).val() == "") {
                divs.show();
                el2.hide();
            }
    });

    home = function(){
        postPage = $("#postPage").hide();
        dataPage = $("#data").show();
        data2Page = $("#data2").hide();
        $("#search").show();
        $('.el').show();
        $('.el2').hide();
        backButton.hide();
        logOut.show();
    }

    back = function(id, isFolder, isActivity){
        getProject(items, id, isFolder, isActivity);
        //getNodes(id, isFolder, isActivity);
    }
    var result = [];
    function setChildParent(source){
        for (key in source){
            var item = source[key];
            result.push({ parent: item, child: item.nodes});
            if(item.nodes){
                setChildParent(item.nodes);
            }
        }
    }
    setChildParent(data.nodes);

    function getParent(id, isFolder, isActivity){
        var project=true;
        for (key in result){
            if(result[key].child){
                for (v in result[key].child){
                    //alert(result[key].child[v].text);
                    if (result[key].child[v].id==id && result[key].child[v].isFolder==isFolder && result[key].child[v].isActivity==isActivity){
                        //alert(result[key].parent.text);
                        return result[key].parent;
                        project=false;
                    }
                }
            }
        }
        if (project){
            return "project";
        }

    }

    });

