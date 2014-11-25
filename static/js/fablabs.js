var _id;
var username;
var fablabs;
var join   ="<button class='btn btn-sm btn-primary btn-action btn-join'>Join</button>";
var leave ="<button class='btn btn-sm btn-danger btn-action btn-leave'>Leave</button>";
var cancel   ="<button class='btn btn-sm btn-warning btn-action btn-cancel'>Cancel</button>";

$(document).ready(function(){
	
	$("#li_fablabs").attr("class","active");



	username     = getCookie("username");
	
	var request1 = getFabber(username);
	request1.done(function(data,jqxhr,status){
		_id        = data._id;
		username   = data.username;
		fablabs = data.fablabs;
	});
	
	var request2 = getFablabs();
	request2.done(function(data,jqxhr,status){
		printFablabs(data);
	});


});

function printFablabs(fablabs){
	$(".box-fablab-view").empty();
	$(fablabs).each(function(){
		if(this.members.indexOf(username)!=-1){
			var button=leave;
		}else if(this.requests.indexOf(username)!=-1){
			var button=cancel;
		}else{
			var button=join;
		}
		var t = document.querySelector('#fablabs_template');
		t.content.querySelector('img').src                           = this.photo;
		t.content.querySelector('label').innerText                   = this.name;
		t.content.querySelector(".section-fablab-fablab").innerText  = this.fablab;
		t.content.querySelector(".section-email-fablab").innerHTML   = "<i class='fa fa-envelope-o'></i> "+this.email;
		t.content.querySelector(".section-members-fablab").innerText = this.members.length+" Members";
		t.content.querySelector(".section-join-fablab").innerHTML    = button;
		t.content.querySelector(".btn-action").setAttribute("data-fablab",this.fablab);

		var fablabbox = document.importNode(t.content, true);
		$(".box-fablab-view").append(fablabbox);
	});

	$(".btn-join").on("click",joinFablab);
	$(".btn-leave").on("click",leaveFablab);
	$(".btn-cancel").on("click",cancelRequest);
}



function joinFablab(){
	var section  = $(this);
	var affected = $(this).data("fablab");
	var request3 = join_fablab(username,affected);
	request3.done(function(data,status,jqxhr){
		newbutton=$.parseHTML(cancel)
		$(newbutton).attr("data-fablab",affected);
		$(newbutton).on("click",cancelRequest);
		$(section).replaceWith(newbutton);

	});
}

function cancelRequest(){
	var section  = $(this);
	var affected = $(this).data("fablab");
	var request3 = cancel_request(username,affected);
	request3.done(function(data,status,jqxhr){
		newbutton=$.parseHTML(join)
		$(newbutton).attr("data-fablab",affected);
		$(newbutton).on("click",joinFablab);
		$(section).replaceWith(newbutton);

	});
}
function leaveFablab(){
	var section  = $(this);
	var fablabname = $(this).data("fablab");
	var request3 = leave_fablab(username,fablabname);
	request3.done(function(data,status,jqxhr){
		newbutton=$.parseHTML(join)
		$(newbutton).attr("data-fablab",fablabname);
		$(newbutton).on("click",joinFablab);
		$(section).replaceWith(newbutton);

	});
}
