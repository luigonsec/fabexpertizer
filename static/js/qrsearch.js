$(document).ready(function(){
	$("#li_qrsearch").attr("class","active");
	$("#results").hide();
	function clean(){
		$("#results").show();
		$("#title_result").empty();
		$("#author_result").html("<label>Author: </label>");
		$("#machine_result").html("<label>Machine: </label>");
		$("#created_result").html("<label>Created: </label>");
		$("#link_result").html("<label>URI: </label>");
	}

	 $('#reader').html5_qrcode(function(data){
 		url=data.split("/fabexs/");
 		if(url.length > 1){
 			fabexs=getFabex(url[1]);
 			fabexs.done(function(data,textStatus,jqXHR){
 				clean();
 				date=new Date(data.created.$date);
 				$("#title_result").append("<label>"+data.title+"</label>");
  				$("#author_result").append(" "+data.author);
 				$("#machine_result").append(" "+data.machine);
 				$("#created_result").append(" "+date.getDate()+"/"+(date.getMonth()+1)+"/"+date.getFullYear());
 				$("#link_result").append("<a href="+location.origin+"/blog/"+data._id+"> Visitar </a>");
 			});
 			
 		}

 	},
 	function(error){
		//show read errors 
	}, function(videoError){
		//the video stream could be opened
	}
);

});