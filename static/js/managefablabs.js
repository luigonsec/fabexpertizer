var photo;
var upload=false;

$(document).ready(function(){
	$(".volatile").hide();
	$("#option-create-fablab").show();
	$("li[data-option='option-create-fablab']").addClass("active");
	$("#li_superuser").attr("class","active");
	$("#li_manage_fablabs").attr("class","active");
	$(".option-fablab-superuser").on("click",changeFablabOption);
	$("#btn-fablab-superuser").on("click",registerFablab);
	$("#btn-grant").on("click",grantPriviliges);
	$("#photo-fablab-superuser").on("change",preparePhoto);
	
	loadFablabs();
	loadFabbers();
});

function changeFablabOption(){
	$(".volatile").hide();
	$(".option-fablab-superuser").removeClass("active");
	$(this).addClass("active");
	id=$(this).data("option");
	$("#"+id).show();
}
function registerFablab(){

	var name        =$("#name-fablab-superuser").val().trim();
	var fablab      =$("#fablab-fablab-superuser").val().trim();
	var description =$("#description-fablab-superuser").val().trim();
	var address     =$("#address-fablab-superuser").val().trim();
	var phone       =$("#phone-fablab-superuser").val().trim();
	var email       =$("#email-fablab-superuser").val().trim();
	var patt_fablab =/^[a-z\d_]{4,15}$/ 
	var patt_name   =/^[a-zA-Z\s\d_]{4,25}$/i  
	var patt_email  =/^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,3})$/  

	var msgerror    ="";
	var errors      =0;

	if(!patt_name.test(name)){
		msgerror+="Specified name invalid.<br>";
		errors++;
	}
	if(!patt_fablab.test(fablab)){
		msgerror+="Specified fablab invalid.<br>";
		errors++;
	}
	if(!patt_email.test(email)){
		msgerror+="Specified email invalid.<br>";
		errors++;
	}
	if (errors){
		alertify.error(msgerror)
		return;
	}

	var json={};
	json.name=name;
	json.fablab=fablab;
	json.email=email;
	
	if(phone.length!=0){
		json.phone=phone;
	}
	
	if(address.length!=0){
		json.email=email;
	}
	
	if(description.length!=0){
		json.description=description;
	}

	var request=postFablab(json)
	request.done(function(data,status,jqxhr){
		alertify.success("Fablab registered")
		if(upload){	
			
			uploadPhoto(fablab); 
		}
		$('#create-fablab-superuser').each (function(){
		  this.reset();
		});

	});
	request.fail(function(data,status,jqxhr){
		if(data.status==409){
			alertify.error("Fablab name already in use");
		}else{
			alertify.error("Some property was not indicated");
		}

	});
}

    function preparePhoto(event){
        photo  = event.target.files;
        if(photo.length != 0){
        	upload = true;
    	}else{
    		upload = false;
    	}
    }


    function uploadPhoto(fablab){
        var formData = new FormData();
        formData.append("file", photo[0]);
        request=$.ajax({
          url: "./api/v1/fablab/photo/"+fablab,
          type: "PUT",
          data: formData,
          processData: false,  // tell jQuery not to process the data
          contentType: false   // tell jQuery not to set contentType
        });
    }

    function loadFablabs(){
    	var request=getFablabs();
    	request.done(function(data,status,jqxhr){
    		fablabs = {}
    		fablabs.fablabs=data;
			var template = $('#fablabsSelect').html();
    		var html = Mustache.to_html(template, fablabs);
    		$('#fablabsSelectDiv').append(html);    		
    	});
    }

    function loadFabbers(){
    	var request=getFabbers();
    	request.done(function(data,status,jqxhr){
    		fabbers = {}
    		fabbers.fabbers=data;
			var template = $('#fabbersSelect').html();
    		var html = Mustache.to_html(template, fabbers);
    		$('#fabbersSelectDiv').append(html);    		
    	});
    }
    
    function grantPriviliges(){
    	var fablab = $("select[name='fablab']").val();
    	var fabber = $("select[name='fabber']").val();
    	var request= grantFabber(fabber,fablab)
    	request.done(function(data,status,jqxhr){
    		alertify.success("Administrator privileges granted to "+fabber+" about "+fablab);
    	});
    	request.fail(function(data,status,jqxhr){
    		alertify.error(data.responseJSON.reason);
    	});

    }