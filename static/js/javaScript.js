
     var loc=location.origin;
$(document).ready(function(){

    $("#bookmarkme").click(function() {
        if (window.sidebar && window.sidebar.addPanel) { // Mozilla Firefox Bookmark
            window.sidebar.addPanel(document.title,window.location.href,'');
        } else if(window.external && ('AddFavorite' in window.external)) { // IE Favorite
            window.external.AddFavorite(location.href,document.title);
        } else if(window.opera && window.print) { // Opera Hotlist
            this.title=document.title;
            return true;
        } else { // webkit - safari/chrome
            alert('Press ' + (navigator.userAgent.toLowerCase().indexOf('mac') != - 1 ? 'Command/Cmd' : 'CTRL') + ' + D to bookmark this page.');
        }
    });
    $('#log-out').on('click',function(){
        setCookie("fabexpertizersession","value",-1);
        setCookie("session","value",-1);
        setCookie("surname","value",-1);
        setCookie("username","value",-1);
        window.location.replace(loc);
                     
    });
});

    // W3 school cookies code
        function setCookie(cname, cvalue, exdays) {
            var d = new Date();
            d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
            var expires = "expires=" + d.toGMTString();
            document.cookie = cname + "=" + cvalue + "; " + expires;
        }

        function getCookie(cname){
            if (cname=="username"){
                var res = getDataSession(cname);
                return res;
            }
            var name = cname + "=";
            var ca = document.cookie.split(';');
            for (var i = 0; i < ca.length; i++){
                var c = ca[i].trim();
                if (c.indexOf(name) == 0)
                    return c.substring(name.length, c.length);
            }
            return "";
        }

        function checkCookie(){
            var user = getCookie("username");
            if (user != ""){
                alert("Welcome again " + user);
            }
            else{
                user = prompt("Please enter your name:", "");
                if (user != "" && user != null){
                    setCookie("username", user, 365);
                }
            }
        }

        function getDataSession(info){
            var request=$.ajax({
                url : loc+"/api/v1/session/"+info,
                type: "GET",
                contentType: "application/json",
                async: false
            });
            var res;
            request.done(function(data,status,jqxhr){
                res = data.param;
            });
            request.fail(function(data,status,jqxhr){
                res = null;
            });
            return res;
        }

        function getDateHour(date){
            pydate=new Date(date.$date);
            var minutes=pydate.getMinutes()
            if(minutes<10){
                minutes="0"+minutes;
            }
            var date=pydate.getDate()+"/"+(pydate.getMonth()+1)+"/"+pydate.getFullYear()+"   "+pydate.getHours()+":"+minutes;    
            return date;
        }
    // End W3 school cookies code
    // Delete cookies code
        $(window).bind("beforeunload", function() { 
            setCookie("name","value",-1);
        });
    // End delete ccokies code
                  
    // API conection code
        function getComments(id){
            var request=$.ajax({
                url: loc+"/api/v1/comments/"+parseInt(id),
                type: "GET",
                contentType: "application/json"
            });
            return request;
        }

        function getCommentsUsername(username){
            var request=$.ajax({
                url: loc+"/api/v1/comments/"+username,
                type: "GET",
                contentType: "application/json"
            });
            return request;
        }   
        
        function put_follow(fabber,followed){
            var request=$.ajax({
                url: loc+"/api/v1/fabber/"+fabber+"/follow/"+followed,
                type: "PUT",
                contentType: "application/json"

            });
            return request;
        }

        function put_unfollow(fabber,unfollowed){
            var request=$.ajax({
                url: loc+"/api/v1/fabber/"+fabber+"/unfollow/"+unfollowed,
                type: "PUT",
                contentType: "application/json"
            });
            return request;
        }

        function postComment(username,oid,comment){
            var json={}
            json.comment=comment

            var request=$.ajax({
                url: loc+"/api/v1/comments/"+username+"/"+oid,
                type: "POST",
                data: JSON.stringify(json),
                contentType: "application/json"
            });
            return request;
        }
        function getFabber(username){
            var request=$.ajax({
                url: loc+"/api/v1/fabbers/"+username,
                type: "GET",
                contentType: "application/json"
            });
            return request;
        }
        
        function getFabbers(sort,order){
            if(sort && order){
                var q="?sort="+sort+"&order="+order;
                console.log(q);
            }else{
                var q="";
            }

            var request=$.ajax({
                url: loc+"/api/v1/fabbers"+q,
                type: "GET",
                contentType: "application/json"
            });
            return request;
        }
        
        function postFabber(name, surname, username, email, password){
            var fabber='{"name":"'+name+'","surname": "'+surname+'","username":"'+username+'", "email": "'+email+'", "password":"'+password+'"}';
            var request=$.ajax({
                url: loc+"/api/v1/fabbers",
                type: "POST",
                data: fabber,
                contentType: "application/json"
            });
            return request;
        }
        function patchFabberPass(username,currentpass,newpass){
            var fabber='{"new_password" : "'+newpass+'", "password" : "'+currentpass+'"}';
            var request=$.ajax({
                url: loc+"/api/v1/fabbers/"+username,
                type: "PATCH",
                data: fabber,
                contentType: "application/json"
            });
            return request;
        }   
        function patchFabberAdmin(fabber){
            var fabberJson=JSON.stringify(fabber);
            var request=$.ajax({
                url: loc+"/api/v1/fabbers/"+fabber.username,
                type: "PATCH",
                data: fabberJson,
                contentType: "application/json"
            });
            return request;
        }
        function patchFabber(name,surname,username,email,password){
            var fabber='{"name":"'+name+'","surname": "'+surname+'","username":"'+username+'", "email": "'+email+'", "password":"'+password+'"}';
            var request=$.ajax({
                url: loc+"/api/v1/fabbers/"+username,
                type: "PATCH",
                data: fabber,
                contentType: "application/json"
            });
            return request;
        }
        
        function deleteFabber(username){
            var request=$.ajax({
                url: loc+"/api/v1/fabbers/"+username,
                type: "DELETE",
                contentType: "application/json"
            });
            return request;
        }
        
        function deleteFabbers(){
            var request=$.ajax({
                url: loc+"/api/v1/fabbers",
                type: "DELETE",
                contentType: "application/json"
            });
            return request;
        }
        
        function getFablabs(){
            var request=$.ajax({
                url: loc+"/api/v1/fablabs",
                type: "GET",
                contentType: "application/json"
            });
            return request;
        }

        function getFabberFablabs(username){
            var request=$.ajax({
                url: loc+"/api/v1/fabbers/"+username+"/fablabs",
                type: "GET",
                contentType: "application/json"
            });
            return request;
        }

        function getFablabMembers(fablab){
            var request=$.ajax({
                url: loc+"/api/v1/fablabs/"+fablab+"/members",
                type: "GET",
                contentType: "application/json"
            });
            return request;
        }

        function getFabberBelt(username){
            var request=$.ajax({
                url: loc+"/api/v1/fabbers/"+username+"/belt",
                type: "GET",
                contentType: "application/json"
            });
            return request;
        }  
        
        
        function postFablab(fablab){
            json=JSON.stringify(fablab);
            var request=$.ajax({
                url: loc+"/api/v1/fablabs",
                type: "POST",
                contentType: "application/json",
                data: json
            });
            return request;
        }
        
        function join_fablab(username,fablab){
            var request=$.ajax({
                url: loc+"/api/v1/fabbers/"+username+"/requests/"+fablab,
                type: "PUT",
                contentType: "application/json"
            });
            return request;
        }

        function cancel_request(username,fablab){
            var request=$.ajax({
                url: loc+"/api/v1/fabbers/"+username+"/requests/"+fablab,
                type: "DELETE",
                contentType: "application/json"
            });
            return request;
        }

        function cancel_request2(username){
            var request=$.ajax({
                url: loc+"/api/v1/fablab/cancel/"+username,
                type: "PUT",
                contentType: "application/json"
            });
            return request;
        }

        
        function accept_request(username,fablab){
            var request=$.ajax({
                url: loc+"/api/v1/fablab/accept/"+username,
                type: "PUT",
                contentType: "application/json"
            });
            return request;
        }
        
        function leave_fablab(username,fablab){
            var request=$.ajax({
                url: loc+"/api/v1/fabbers/"+username+"/leave/"+fablab,
                type: "PUT",
                contentType: "application/json"
            });
            return request;
        }

        function getFabex(id){
            var request=$.ajax({
                url: loc+"/api/v1/fabexs/"+id,
                type: "GET",
                async: false,
                contentType: "application/json"
            });
            return request;
        }
        function getFabexs(busqueda){
            var filtro="";
            if(busqueda != null){
                filtro="?q="+busqueda;
            }
            var request=$.ajax({
                url: loc+"/api/v1/fabexs"+filtro,
                type: "GET",
                contentType: "application/json"
            });
            return request;
        }
        
        function getFabexsFromFabber(username){
            var request=$.ajax({
                url: loc+"/api/v1/fabbers/"+username+"/fabexs",
                type: "GET",
                contentType: "application/json"
            });
            return request;
        }

        function grantFabber(fabber,fablab){
            var request=$.ajax({
                url: loc+"/api/v1/fabbers/"+fabber+"/grant/"+fablab,
                type: "PATCH",
                contentType: "application/json"
            });
            return request;
        }

        function postFabex(fabex){
            var fabexJson=JSON.stringify(fabex);
            var request=$.ajax({
                url: loc+"/api/v1/fabexs",
                type: "POST",
                data: fabexJson,
                timeout: 10000,
                contentType: "application/json"
            });
            return request;
        }
        function patchFabex(fabex){
            var fabexJson=JSON.stringify(fabex);
            var request=$.ajax({
                url: loc+"/api/v1/fabexs/"+fabex.id,
                type: "PATCH",
                data: fabexJson,
                contentType: "application/json"
            });
            return request;
        }
        function deleteFabex(id){
            var request=$.ajax({
                url: loc+"/api/v1/fabexs/"+id,
                type: "DELETE",
                contentType: "application/json"
            });
            return request;
        }
        function deleteFabexs(){
            var request=$.ajax({
                url: loc+"/api/v1/fabexs",
                type: "DELETE",
                contentType: "application/json"
            });
            return request;
        }
    function getMaterials(){
        var request=$.ajax({
            url: loc+"/api/v1/materials",
            type: "GET",
            contentType: "application/json"
        });
        return request;
    }
    function getMaterial(material){
        var request=$.ajax({
            url: loc+"/api/v1/materials/"+material,
            type: "GET",
            contentType: "application/json"
        });
        return request;
    }
function postMaterial(material){
    var materialJson=JSON.stringify(material);
    var request=$.ajax({
                       url: loc+"/api/v1/materials",
                       type: "POST",
                       data: materialJson,
                       contentType: "application/json"
                       });
    return request;
}

function patchMaterial(material){
    var materialJson=JSON.stringify(material);
    var request=$.ajax({
                       url: loc+"/api/v1/materials",
                       type: "PATCH",
                       data: materialJson,
                       contentType: "application/json"
                       });
    return request;
}

function deleteMaterial(name){
    var request=$.ajax({
                       url: loc+"/api/v1/materials/"+name,
                       type: "DELETE",
                       contentType: "application/json"
                       });
    return request;
}
function deleteMaterials(){
    var request=$.ajax({
                       url: loc+"/api/v1/materials",
                       type: "DELETE",
                       contentType: "application/json"
                       });
    return request;
}
function getMachines(){
    var request=$.ajax({
                       url: loc+"/api/v1/machines",
                       type: "GET",
                       contentType: "application/json"
                       });
    return request;
}
function getMachine(machine){
    var request=$.ajax({
                       url: loc+"/api/v1/machines/"+machine,
                       type: "GET",
                       contentType: "application/json"
                       });
    return request;
}
function postMachine(machine){
    var machineJson=JSON.stringify(machine);
    var request=$.ajax({
                       url: loc+"/api/v1/machines",
                       type: "POST",
                       data: machineJson,
                       contentType: "application/json"
                       });
    return request;
}

function patchMachine(machine){
    var machineJson=JSON.stringify(machine);
    var request=$.ajax({
                       url: loc+"/api/v1/machines/"+machine.name,
                       type: "PATCH",
                       data: machineJson,
                       contentType: "application/json"
                       });
    return request;
}

function deleteMachine(name){
    var request=$.ajax({
                       url: loc+"/api/v1/machines/"+name,
                       type: "DELETE",
                       contentType: "application/json"
                       });
    return request;
}
function deleteMachines(){
    var request=$.ajax({
                       url: loc+"/api/v1/machines",
                       type: "DELETE",
                       contentType: "application/json"
                       });
    return request;
}


function uploadFileExample(){
    var formData = new FormData();
    formData.append("username", "Groucho");
    formData.append("accountnum", 123456); // number 123456 is immediately converted to string "123456"
    // HTML file input user's choice...
    formData.append("userfile", fileInputElement.files[0]);
    // JavaScript file-like object...
    var content = '<a id="a"><b id="b">hey!</b></a>'; // the body of the new file...
    var blob = new Blob([content], { type: "text/xml"});
    formData.append("webmasterfile", blob);
    var request = new XMLHttpRequest();
    request.open("POST", "http://foo.com/submitform.php");
    request.send(formData);
}


function postSource(source,id){
    var data = new FormData();
    data.append('file', source,source.name);
    var request = new XMLHttpRequest();
    request.open("PATCH", loc+"/api/v1/source/"+id, true);
    request.send(data);
    return request;
}


/** 
#################################################
####     ESTA PARTE NO LLEGÓ A FUNCIONAR     ####
#################################################


function postFront(front,id){
    var blob = new Blob([front], { type: "image/webp"});
    var data = new FormData();
    data.append('file', blob, 'front'+id);
    var request = new XMLHttpRequest();
    request.open("PATCH", loc+'/api/v1/images/'+id+'/front',true);
    request.send(data);
    return request;
}
function postTop(top,id){
    var blob = new Blob([top], { type: "image/webp"});
    var data = new FormData();
    data.append('file', blob,'top'+id);
    var request = new XMLHttpRequest();
    request.open("PATCH", loc+'/api/v1/images/'+id+'/top',true);
    request.send(data);
    return request;
}
function postLeft(left,id){
    var blob = new Blob([left], { type: "image/webp"});
    var data = new FormData();
    data.append('file', blob,'left'+id);
    var request = new XMLHttpRequest();
    request.open("PATCH", loc+'/api/v1/images/'+id+'/left',true);
    request.send(data);
    return request;
}
**/

function patchLike(username,oid){
    var request=$.ajax({
                       url: loc+"/api/v1/fabexs/like/"+username+"/"+parseInt(oid),
                       type: "PATCH",
                       contentType: "application/json"
                       });
    return request;
}

function patchDislike(username,oid){
    var request=$.ajax({
                       url: loc+"/api/v1/fabexs/dislike/"+username+"/"+parseInt(oid),
                       type: "PATCH",
                       contentType: "application/json"
                       });
    return request;
}











    // End API conection code