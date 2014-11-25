$(document).ready(function(){

	$(".accept-user").on("click",aceptarUsuario);
	$(".cancel-user").on("click",cancelarUsuario);
	
})

function aceptarUsuario(){
	var username = $(this).data("user");
	var request = accept_request(username);
	request.done(function(data,status,jqxhr){
		if (data.ok){
			alertify.log("success",username+" added.",0)
			$("#"+username+"-request").remove();
		}
	});
	request.fail(function(data,status,jqxhr){
		alertify.log("error");
	});

}

function cancelarUsuario(){
	var username = $(this).data("user");
	var request = cancel_request2(username);
	request.done(function(data,status,jqxhr){
		if (data.ok){
			alertify.log("success",username+" refused.",0)
			$("#"+username+"-request").remove();
		}
	});
	request.fail(function(data,status,jqxhr){
		alertify.log("error");
	})
	
}