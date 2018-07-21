$(document).ready(function () {  
  
    function getRootmenu() {  
        $.ajax({  
            type: "get",  
            dataType: "json",  
            url: "/common/getmenu",  
            success: function (data) {  
                var m = "";  
                if (data.size > 0) {  
                    for (j = 0; j < data.size; j++) {  
                        if (data.menus_node[j].parent_id == -1) {  
                            if (data.menus_node[j].ishas_son == 1) {  
                                m = m + "<li roletype='2' id='" + data.menus_node[j].node_id + "' class='dropDown dropDown_hover'>" +  
                                    "<a class='dropDown_A' href='" + data.menus_node[j].node_url + "'>" + data.menus_node[j].node_showname + "<i class='Hui-iconfont' >" + '' + "</i></a></li>";  
  
                            }  
                            else {  
                                m = m + "<li roletype='2' id='" + data.menus_node[j].node_id + "' class='dropDown dropDown_hover'>" +  
                                    "<a class='dropDown_A' href='" + data.menus_node[j].node_url + "'>" + data.menus_node[j].node_showname + "</a></li>";  
  
                            }  
                        }  
                    }  
                }  
                $('#ulmenu').html(m);  
                $("#ulmenu li").bind('mouseover', function (e) {  
                    getSonMenu(this, e)  
                });  
            }  
        });  
    }  
    getRootmenu();  
  
  
    function getSonMenu(event) {  
        var parentId = $(event).attr("id");  
        var roletype = $(event).attr("roletype");  
        if (roletype == "2")  
            $(event).addClass("hover open");  
        if (roletype == "1")  
            $(event).addClass("open");  
        if ($(event).find("li").length > 0 || roletype == "0") return;  
        $.ajax({  
            type: "get",  
            dataType: "json",  
            url: "/common/getSonMenu?parentId=" + parentId,  
            success: function (result) {  
                var parentId = $(event).attr("id");  
                $('#' + parentId).html($('#' + parentId + ' >a'))  
                // $('#'+parentId).html("");  
                var a = "<ul class='dropDown-menu menu radius box-shadow'>";  
                var b = "</ul>";  
                var c = "";  
                $.each(result, function (i) {  
                    if(result[i].isnewblank == 1 && result[i].ishas_son == 1)  
                        {  
                            c = c + "<li roletype='" + result[i].ishas_son + "' id=" + result[i].node_id + "><a href='" + result[i].node_url + "' target='_blank'>" + result[i].node_showname + "<i class='arrow Hui-iconfont'></i></a></li>";  
                        }  
                    if(result[i].isnewblank == 1 && result[i].ishas_son == 0){  
                            c = c + "<li roletype='" + result[i].ishas_son + "' id=" + result[i].node_id + "><a href='" + result[i].node_url + "' target='_blank'>" + result[i].node_showname + "</a></li>";  
                    }  
                    if(result[i].isnewblank == 0 && result[i].ishas_son == 1){  
                            c = c + "<li roletype='" + result[i].ishas_son + "' id=" + result[i].node_id + "><a href='" + result[i].node_url + "'>" + result[i].node_showname + "<i class='arrow Hui-iconfont'></i></a></li>";  
                    }  
                    if(result[i].isnewblank == 0 && result[i].ishas_son == 0){  
                            c = c + "<li roletype='" + result[i].ishas_son + "' id=" + result[i].node_id + "><a href='" + result[i].node_url + "'>" + result[i].node_showname + "</a></li>";  
                    }  
                });  
                $('#' + parentId).append(a + c + b);  
                $("#ulmenu li").unbind('mouseover');  
                $("#ulmenu li").bind('mouseover', function (e) {  
                    getSonMenu(this, e)  
                });  
            }, error: function (result) {  
                alert(result.responseText);  
            }  
        });  
    }  
  
}); 