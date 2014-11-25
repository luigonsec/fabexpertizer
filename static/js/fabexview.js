$(document).ready(function(){        
	$("#li_blog").attr("class","active");

   	buttonLike="<button class='btn btn-sm btn-primary' id='like'><i class='fa fa-thumbs-up'></i> I like</button>"
    buttonDislike="<button class='btn btn-sm btn-danger' id='dislike'><i class='fa fa-thumbs-down'></i> I don't like</button>"
    buttonDelete="<button class='btn btn-sm btn-danger' id='delete'><i class='fa fa-trash'></i> Remove fabex</button>"

    var path=location.pathname.split('/');
    var oid=path[2]
		var request=getFabex(Number(oid));
        request.done(function(data, textStatus, jqXHR){
            showFabex(Number(oid));
            showComments(Number(oid));
        });
        request.fail(function(jqXHR, textStatus, errorThrown){
            alert("Some error ocurr");
        });

		$('#qr').qrcode({
			size: 235,		
			color: '#3a3',
			text: 'http://fabexpertizer.herokuapp.com/api/v1/fabexs/'+oid
		});

    $("#delete").on('click',function(){
    	var request=deleteFabex(oid);
    	request.done(function(data,textStatus,jqXHR){
			$(location).attr('href',location.origin+'/blog');
    	});
    });



    $("#send-comment").on('click',function(){
        username=getCookie("username");
        comment=$("#text-comment").val();
        var request=postComment(username,Number(oid),comment);
        request.done(function(data,textStatus,jqXHR){
            showComments(oid);
        });
        request.fail(function(a,b,c){
            alertify.error("No se pudieron cargar los comentarios.")
        })
    });



    });

function showFabex(id){
    var request=getFabex(id);
    username=getCookie("username")
    request.done(function(data, textStatus, jqXHR){
        $("#title").append(data.title);
        $("#author").append(data.author);
        $("#description").append(data.description);
        $("#machine").append(data.machine);
        if (data.top === undefined){
            $("#top").attr('src',location.origin+"/inmg/no-photo.svg");
        }else{
            $("#top").attr('src',"../"+data.top);
        }       
        if (data.left === undefined){
            $("#left").attr('src',location.origin+"/inmg/no-photo.svg");
        }else{
            $("#left").attr('src',"../"+data.left);
        }
        if (data.front === undefined){
            $("#front").attr('src',location.origin+"/inmg/no-photo.svg");
        }else{
            $("#front").attr('src',"../"+data.front);
        }    

        $("#current_breadcrumb").append(data.title);
        if(data.source){
            $("#download").attr("href",location.origin+"/"+data.source);
        }else{
            $("#source_button").remove()
        }
        if (data.likes === undefined){
            $("#likes_count").append("0 likes.");
        }else{
            $("#likes_count").append(data.likes.length+" likes.");
        }
        if($.inArray(username,data.likes) != -1){
           	$("#like_button").html(buttonDislike);
            $("#dislike").click(click_dislike(id));
        }else if(data.author == username){
           	$("#like_button").hide();
           	$("#delete_button").html(buttonDelete);
            $("#dislike").click(click_dislike(id));

        }else{
           	$("#like_button").html(buttonLike);
            $("#like").click(click_like(id));
        }
        div='<p class="list-group-item" id="machine"><label>Machine:</label>'+data.machine+'</p>';
        for(var i=0;i<data.properties.length;i++){
            div=div+'<p class="list-group-item"><label>'+data.properties[i].name+': </label> '+data.properties[i].value+'</p>';
         }
         $('#properties').append(div);
    });

}
function showComments(id){
    var comments=getComments(id);
    comments.done(function(data, textStatus, jqXHR){
        $(".list-comments").empty();
        $(data).each(function(){
            var elemento="<li class='list-group-item comment'><label class='info-comment'>"+this.username+"</label><p class='body-comment'>"+this.comment+"</p></li>"
            $(".list-comments").append(elemento);
        });
    });
};

function click_like(oid){
    $("#like").on('click',function(){
        username=getCookie("username");
        var request=patchLike(username,oid);
        request.done(function(data,textStatus,jqXHR){
            $("#like_button").html(buttonDislike);
            $("#dislike").click(click_dislike(oid))

        });

    });
}

function click_dislike(oid){
    $("#dislike").on('click',function(){
        username=getCookie("username");
        var request=patchDislike(username,oid);
        request.done(function(data,textStatus,jqXHR){
            $("#like_button").html(buttonLike);
            $("#like").click(click_like(oid));
        });

    });
}