var _id;
var username;
var followings;
var follow   ="<button class='btn btn-sm btn-primary btn-action btn-follow'>Follow</button>";
var unfollow ="<button class='btn btn-sm btn-danger btn-action btn-unfollow'>Unfollow</button>";

$(document).ready(function(){
	
	$("#li_fabbers").attr("class","active");


	username     = getCookie("username");
	
	var request1 = getFabber(username);
	request1.done(function(data,jqxhr,status){
		_id        = data._id;
		username   = data.username;
		followings = data.followings;
		var request2 = getFabbers();
		request2.done(function(data,jqxhr,status){
			printFabbers(data);
		});

	});
	


	$("#sort-input-fabber, #order-input-fabber").on("change",function(){
		var order  = $("#order-input-fabber").val();
		var sort = $("#sort-input-fabber").val();
		console.log(sort);
		console.log(order);
		request2 = getFabbers(sort,order);
		request2.done(function(data,jqxhr,status){
			printFabbers(data);
		})
	});



});



function printFabbers(fabbers){
	$(".box-fabber-view").empty();
	$(fabbers).each(function(){
		if(followings.indexOf(this.username)==-1){
			var button=follow;
		}else{
			var button=unfollow;
		}

		if(username!=this.username){
			var t = document.querySelector('#fabbers_template');
			t.content.querySelector('img').src = this.photo;
			t.content.querySelector('label').innerHTML						= "<a href='./fabbers/"+this.username+"'>"+this.name+" "+this.surname+"</a>";
			t.content.querySelector(".section-fabexs-fabber").innerText     = this.fabexs.length+" fabexs";
			t.content.querySelector(".section-comments-fabber").innerText   = this.comments.length+" comments";
			t.content.querySelector(".section-username-fabber").innerText   =  					  this.username;
			t.content.querySelector(".section-follow-fabber").innerHTML     = 					  button;
			t.content.querySelector(".btn-action").setAttribute("data-user",this.username);

			var fabberbox = document.importNode(t.content, true);
			$(".box-fabber-view").append(fabberbox);
		}
	});

	$(".btn-follow").on("click",followUser);
	$(".btn-unfollow").on("click",unfollowUser);
}


function unfollowUser(){
	var section  = $(this);
	var affected = $(this).data("user");
	var request3 = put_unfollow(username,affected);
	request3.done(function(data,status,jqxhr){
		newbutton=$.parseHTML(follow)
		$(newbutton).attr("data-user",affected);
		$(newbutton).on("click",followUser);
		$(section).replaceWith(newbutton);

	});
}
function followUser(){
	var section  = $(this);
	var affected = $(this).data("user");
	var request3 = put_follow(username,affected);
	request3.done(function(data,status,jqxhr){
		newbutton=$.parseHTML(unfollow)
		$(newbutton).attr("data-user",affected);
		$(newbutton).on("click",unfollowUser);
		$(section).replaceWith(newbutton);

	});
}
