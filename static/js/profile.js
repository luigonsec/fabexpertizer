var _id;
var username;
var followings;
var follow   ="<button class='btn btn-primary btn-action btn-follow'>Follow</button>";
var unfollow ="<button class='btn btn-primary btn-action btn-unfollow'>Unfollow</button>";

$(document).ready(function(){
	
	$("#li_fabbers").attr("class","active");
	var path=location.pathname.split('/');
	username=path[path.length-1];
	var request=getFabber(username);
	request.done(function(data,status,jqxhr){
		$("#photo-profile").attr("src","../"+data.photo);
		$("#name-fabber-profile").html("<h3>"+data.name+" "+data.surname+"</h3>");
		$("#username-fabber-profile").html("<label>"+data.username+"</label>");
		requestBelt=getFabberBelt(username);
		requestBelt.done(function(data,status,jqxhr){
			$("#belt").addClass(data.belt);
		})
	});
	loaduserfabexs();
	loaduserfabelabs();


});

	function loaduserfabexs(){
		var request=getFabexsFromFabber(username)
		request.done(function(data,status,jqxhr){
			json={}
			json.fabexs=data
			printuserfabexs(json)

			
		})
	}
	function printuserfabexs(fabexs){
		var template = $('#userfabexs').html();
		var html = Mustache.to_html(template, fabexs);
		$('#fabexssection').html(html);
	}

	function loaduserfabelabs(){
		var request=getFabberFablabs(username)
		request.done(function(data,status,jqxhr){
			json={}
			json.fablabs=data
			var template = $('#userfablabs').html();
    		var html = Mustache.to_html(template, json);
    		$('#fablabssection').html(html); 
			
		})
	}

	function loaduserfollowers(){
		var request=getFabexsFromFabber(username)
		request.done(function(data,status,jqxhr){
			json={}
			json.fabexs=data
			var template = $('#userfabexs').html();
    		var html = Mustache.to_html(template, fabexs);
    		$('#userfabexs').html(html); 
			
		})
	}