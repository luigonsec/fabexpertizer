$(document).ready(function(){
    $("#li_blog").attr("class","active")
    var filt=null;
    loadBlog();
    $('.filter').on('click',function(){
            filt=$(this).attr('cat');
            var request=getFabexs();
            request.done(function(data, textStatus, jqXHR){
                var blogFabexs=categoryFilter(data,filt);
                showFabexs(blogFabexs);
            });
            request.fail(function(jqXHR, textStatus, errorThrown){
                alert("Some error ocurr");
            });
        });
    });

$("#btn-search").on('click',function(){
    busqueda=$("#field_search").val();
    console.log("Algo es algo");
    loadBlog(busqueda);
});

function loadBlog(filtro){
    var request=getFabexs(filtro);
    request.done(function(data, textStatus, jqXHR){
        var blogFabexs=filter(data);
        showFabexs(blogFabexs);
        if(filtro){
            $("#search-results").html('Results containing "'+filtro+'". <a href="'+location.origin+'/blog">Restart</a>');
        }
    });
    request.fail(function(data,textStatus,jqXHR){
        if(data.status==404){
            $("#search-results").html('Not element were found containing "'+filtro+'". <a href="'+location.origin+'/blog">Restart</a>');
            showFabexs();
        }else{
            $("#search-results").html('Some wrong happens while finding fabexs containing "'+filtro+'". <a href="'+location.origin+'/blog">Restart</a>');
            showFabexs();
        }

    });
}


function filter(fabexs){
    var filterfabexs= Array();
    for(var i=0;i<fabexs.length;i++){
        if(fabexs[i].blog){
            filterfabexs.push(fabexs[i]);
        }
    }
    return filterfabexs;
}
function categoryFilter(fabexs, category){
    var filterfabexs= Array();
    for(var i=0;i<fabexs.length;i++){
        if(fabexs[i].blog && fabexs[i].machine==category){
            filterfabexs.push(fabexs[i]);
        }
    }
    return filterfabexs;
}

function showFabexs(blogFabexs){
    var i=0;
    $('#fabexs').empty();
    while ( i<blogFabexs.length){
        //Change true for blog property
        if(blogFabexs[i].blog){
            /*
            var div='<div class="row">'+'<div id="fabex'+blogFabexs[i]._id+'" class="col-md-4"><a class="fabex" href="../blog/'+blogFabexs[i]._id+'"  fabex="'+blogFabexs[i]._id+'"><h2>'+blogFabexs[i].title+'</h2></a> by '+blogFabexs[i].author;
            if (!(blogFabexs[i].front === undefined)){
                div=div+'<img id="btn-front" src="'+blogFabexs[i].front+'" alt="The front photo" class="img-thumbnail"></div>';
            }else{
                div=div+'<img id="btn-front" src="./img/no-photo.svg" alt="The front photo" class="img-thumbnail"></div>';
            }

            if(i<blogFabexs.length-1){
                div =div+'<div id="fabex'+blogFabexs[i+1]._id+'" class="col-md-4 col-sm-offset-2"><a class="fabex" href="../blog/'+blogFabexs[i+1]._id+'"  fabex="'+blogFabexs[i+1]._id+'"><h2>'+blogFabexs[i+1].title+'</h2></a> by '+blogFabexs[i+1].author;
                if (!(blogFabexs[i+1].front === undefined)){
                    div=div+'<img id="btn-front" src="'+blogFabexs[i+1].front+'" alt="The front photo" class="img-thumbnail"></div>';
                }else{
                    div=div+'<img id="btn-front" src="./img/no-photo.svg" alt="The front photo" class="img-thumbnail"></div>';
                }
            }
            div=div+'</div>';*/
            if(blogFabexs[i].description.length>15){
                var subStrEnd=20;
            }else{
                var subStrEnd=blogFabexs[i].description.length;
            }
            var div=$('#blog_templates').find('.blog-element').clone();
            $(div).children("div").addClass("border-"+blogFabexs[i].belt)
            div.find('.fabbex-link').attr('href','../blog/'+blogFabexs[i]._id)
            div.find('#fabbex-photo-front').attr('src',blogFabexs[i].front);
            div.find('#fabbex-photo-top').attr('src',blogFabexs[i].top);
            div.find('#fabbex-photo-left').attr('src',blogFabexs[i].left);            
            div.find('.fabbex-title').append(blogFabexs[i].title);
            div.find('.fabbex-fablab').append(blogFabexs[i].fablab);
            div.find('.fabbex-author').append(blogFabexs[i].author);
            div.find('.fabbex-description').append(blogFabexs[i].description.substring(0,subStrEnd)+'...');
            div.find('.fabex-machine').append(blogFabexs[i].machine);
            
            $('#fabexs').append(div);
            
        }
        i=i+1;
    }
}





