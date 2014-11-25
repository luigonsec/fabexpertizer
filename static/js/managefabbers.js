var users=null;


$(document).ready(function(){        
	
	$('#li_superuser').attr("class","active");
	$('#option-profile-fabbers').attr("class","active");
    refreshUsers();
	
	
    $('#table-body').on('click','.delete-user',function(){
        var username=$(this).attr('username');
        var request=deleteFabber(username);
        request.done(function(data, textStatus, jqXHR){
                alertify.success("User delete."); 
                refreshUsers();
                refreshPaginator(10);
        });
        request.fail(function(jqXHR, textStatus, errorThrown){
                alertify.error("User can't be delete.");
                refreshUsers();
        });
    });
	
    $('#table-body').on('click','.remove-admin',function(){
        var user=$(this).attr('username');
        var fabber={username: user, admin:false};
        var request =patchFabberAdmin(fabber);
        request.done(function(data, textStatus, jqXHR){
                alertify.success("User isn't admin now."); 
                refreshUsers();
                refreshPaginator(10);
        });
        request.fail(function(jqXHR, textStatus, errorThrown){
                alertify.error("User can't be downgrade.");
                refreshUsers();
        });
        
    });
    $('#table-body').on('click','.add-admin',function(){
        var user=$(this).attr('username');
        var fabber={username: user, admin:true};
        var request =patchFabberAdmin(fabber);
        request.done(function(data, textStatus, jqXHR){
                alertify.success("User isn admin now."); 
                refreshUsers(10);
                refreshPaginator();
        });
        request.fail(function(jqXHR, textStatus, errorThrown){
                alertify.error("User can't be upgrade.");
                refreshUsers();
        });
    });
    $('#paginator').on('click','.page',function(){
        var page=$(this).attr('page');
        $('#paginator').attr('page',page);
        showFabbers(page*10,10);
        refreshPaginatorArrows(page);
        
    });
    $('#next-page').on('click',function(){
        var page=parseInt($('#paginator').attr('page'))+1;
        $('#paginator').attr('page',page);
        showFabbers(page*10,10);
        
    });
    $('#previous-page').on('click',function(){
        var page=parseInt($('#paginator').attr('page'))-1;
        $('#paginator').attr('page',page);
        showFabbers(page*10,10);
    });
    
});

function refreshUsers(){
    var fabbersRequest=getFabbers();
    fabbersRequest.done(function(data, textStatus, jqXHR){
        users=data;
        showFabbers(0,10);
        refreshPaginator(10);
    });
}

function showFabbers(first, numToShow){
    $('#table-body').find('.user-row').remove();
    var templates=$('#fabber_row_template');
	for (var i = first; i < first+numToShow && i<users.length; i++) {
        
		var row = null;

		if (users[i].admin){
            row = templates.find('.admin-row').clone();
            row.find('.remove-admin').attr('username',users[i].username);
            row.find('.is-admin').append('Yes');
            
		}else{
			row = templates.find('.no-admin-row').clone();
            row.find('.add-admin').attr('username',users[i].username);
            row.find('.is-admin').append('No');
		}
        row.find('.id').append(i);
        row.find('.username').append(users[i].username);
        row.find('.email').append(users[i].email);
        row.find('.delete-user').attr('username',users[i].username);

		$('#paginator-row').before(row);
	}
    refreshPaginatorArrows(first/10);
    
}
function refreshPaginator(numToShow){
    $('#paginator').find('.page').remove();
    var pages=Math.floor(users.length/numToShow);
    if(users.length%numToShow!=0){
        pages=pages+1;
    }
    if (pages>1){
        $('#paginator-row').removeClass('hidden')
        $('#paginator').attr('pages',pages);
        for(var i=0;i<pages;i++){
            var page=$('#fabber_row_template').find('.page').clone();
            page.attr('page',i);
            page.find('a').append(i+1);
            $('#next-page').before(page);
        }
    }
}
function refreshPaginatorArrows(page){
    if(page==0){
        $('#previous-page').addClass('hidden');
        $('#next-page').removeClass('hidden');
    }else if(page==($('#paginator').attr('pages')-1)){
        $('#next-page').addClass('hidden');
        $('#previous-page').removeClass('hidden');
    }else{
        $('#previous-page').removeClass('hidden');
        $('#next-page').removeClass('hidden');
    }
}
