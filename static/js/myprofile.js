var files;
var username;
var email;
var registered;
var request;
var likes;
var photo;

$(document).ready(function(){

	$("#li_profile").attr("class","active");
    username=getCookie("username");
    var request=getFabber(username);
    request.done(function(data,status,jqxhr){
    	likes=data.likes;
        email=data.email;
        registered=getDateHour(data.date);
        photo=data.photo;
        $("#email-modal-profile").html(email);
        $("#registered-modal-profile").html(registered);
        $(".photo-profile").attr("src","../"+photo+"?lastmod="+new Date().toString());

    });

    /********************************/
    /*********  PESTAÑAS   **********/
    /********************************/

    $(".option-profile-item").on("click",select_option_profile);
    $("#option-profile-fabexs").on("click",select_option_profile_fabexs);
    $("#option-profile-likes").on("click",select_option_profile_likes);
    $("#option-profile-comments").on("click",select_option_profile_comments);
    $("#option-profile-followers").on("click",select_option_profile_followers);
    $("#option-profile-followings").on("click",select_option_profile_followings);

    $("#option-profile-fabexs").click()

    /********************************/
    /***********  MODAL   ***********/
    /********************************/
    
    $("#btn-change-password").on("click",changePassword);        
    $("#username-modal-profile").html(username);
    $('input[type=file]').on('change', prepareUpload);


});

	
	function select_option_profile(){    	
		$(".option-profile").children(".active").removeClass("active");
    	$(this).addClass("active");
    }

    function select_option_profile_fabexs(){
        try{
            request.abort();
        }catch(err){

        }
        $("#title-option-profile").html("Fabexs");
        $("#body-option-profile").empty();
   		var container="";
        container+=  "<div class='row container-fabex-profile' id='container-fabex-profile-##oid##'>";
        container+=  "  <div class='col-sm-3'>";
        container+=  "      <div class='row'>";
        container+=  "          <div class='col-sm-12'>";
        container+=  "              <div class='thumbnail'>";
        container+=  "                  <img src='##top##' alt='##description##'>";
        container+=  "              </div>";
        container+=  "          </div>";
        container+=  "      </div>";
        container+=  "  </div>";
        container+=  "  <div class='col-sm-6'>";
        container+=  "      <div class='row'>";
        container+=  "          <div class='col-sm-12'>";
        container+=  "              <h4 class='title-fabex-profile'>##title##</h4>";
        container+=  "              <p>##description##</p>";
        container+=  "              <p>##date##</p>";
        container+=  "          </div>";
        container+=  "      </div>";
        container+=  "  </div>";
        container+=  "  <div class='col-sm-3 buttons-fabex-profile'>";
        container+=  "      <div class='row'>";
        container+=  "          <div class='col-sm-12'>";
        container+=  "              <button class='btn btn-default btn-sm'>";
        container+=  "                  <a href='./blog/##oid##'>Visitar</a>";
        container+=  "              </button>";
        container+=  "              <button class='btn btn-default btn-sm'>";
        container+=  "                  <a href='./blog/##oid##'>Borrar</a>";
        container+=  "              </button>";
        container+=  "          </div>";
        container+=  "      </div>";
        container+=  "  </div>";
        container+=  "</div>";
    	request=getFabexsFromFabber(username)
    	request.done(function(data,status,jqxhr){
            $(data).each(function(){
                var pydate=new Date(this.created.$date)
                var minutes=pydate.getMinutes()
                if(minutes<10){
                    minutes="0"+minutes;
                }
                var date=pydate.getDate()+"/"+(pydate.getMonth()+1)+"/"+pydate.getFullYear()+"   "+pydate.getHours()+":"+minutes;
    			var copy=container
    			copy=copy.replace(/##oid##/g, this._id);
    			copy=copy.replace(/##top##/g, this.top);
    			copy=copy.replace(/##description##/g, this.description);
    			copy=copy.replace(/##title##/g, this.title);
                copy=copy.replace(/##date##/g,date);
                $("#body-option-profile").append(copy)
    		})
    	});
    }
    

    function select_option_profile_likes(){
        try{
            request.abort();
        }catch(err){
            
        }
    	$("#title-option-profile").html("Likes");
        $("#body-option-profile").empty();
        var container="";
        container+=  "<div class='row container-likes-profile' id='container-likes-profile-##oid##'>";
        container+=  "  <div class='col-sm-3'>";
        container+=  "      <div class='row'>";
        container+=  "          <div class='col-sm-12'>";
        container+=  "              <div class='thumbnail'>";
        container+=  "                  <img src='##top##' alt='##description##'>";
        container+=  "              </div>";
        container+=  "          </div>";
        container+=  "      </div>";
        container+=  "  </div>";
        container+=  "  <div class='col-sm-6'>";
        container+=  "      <div class='row'>";
        container+=  "          <div class='col-sm-12'>";
        container+=  "              <h4 class='title-likes-profile'>##title##</h4>";
        container+=  "              <p>##description##</p>";
        container+=  "              <p>##date##</p>";
        container+=  "          </div>";
        container+=  "      </div>";
        container+=  "  </div>";
        container+=  "  <div class='col-sm-3 buttons-likes-profile'>";
        container+=  "      <div class='row'>";
        container+=  "          <div class='col-sm-12'>";
        container+=  "              <button class='btn btn-default btn-sm'>";
        container+=  "                  <a href='./blog/##oid##'>Visitar</a>";
        container+=  "              </button>";
        container+=  "          </div>";
        container+=  "      </div>";
        container+=  "  </div>";
        container+=  "</div>";
        $(likes).each(function(){
            request=getFabex(this);
            request.done(function(data,status,jqxhr){
                $(data).each(function(){
                    var date=getDateHour(this.created)
                    var copy=container;
                    copy=copy.replace(/##oid##/g, this._id);
                    copy=copy.replace(/##top##/g, this.top);
                    copy=copy.replace(/##description##/g, this.description);
                    copy=copy.replace(/##title##/g, this.title);
                    copy=copy.replace(/##date##/g,date);
                    $("#body-option-profile").append(copy);
                })
            });
        });
    }
    function select_option_profile_comments(){
        try{
            request.abort();
        }catch(err){
            
        }
    	$("#title-option-profile").html("Comments");
        $("#body-option-profile").empty();
        var container="";
        container+=  "<div class='row container-comment-profile' id='container-comment-profile-##oid##'>";
        container+=     "<div class='panel panel-default col-sm-10'>";
        container+=         "<div class='panel-body'>";
        container+=         "<p id='text-comment-profile-##oid##'>##text##</p>##date##"
        container+=         "</div>";
        container+=     "<div>";
        container+=  "</div>";
        request=getCommentsUsername(username)
        request.done(function(data,status,jqxhr){
            $(data).each(function(){
                req=getFabex(this.fabex);
                var title;
                req.done(function(data,status,jqxhr){
                    title=data.title;
                });
                var date=getDateHour(this.date) 
                var copy=container;
                text="You wrote <em>'"+this.comment+"'</em> in fabex named <a href=./blog/"+this.fabex+">"+title+"</a>";
                copy=copy.replace(/##oid##/g,this._id);
                copy=copy.replace(/##text##/g,text);
                copy=copy.replace(/##date##/,date);
                $("#body-option-profile").append(copy);
            });
        });
    }
    function select_option_profile_followers(){
        try{
            request.abort();
        }catch(err){
            
        }  	
        $("#title-option-profile").html("Followers")
        $("#body-option-profile").empty();
    }
    function select_option_profile_followings(){
        try{
            request.abort();
        }catch(err){
            
        }   	
        $("#title-option-profile").html("Following")
        $("#body-option-profile").empty();
    }


    function changePassword(){
        var current_password=$("#current-password").val().trim();

        var new_password=$("#new-password").val().trim();
        var verify_password=$("#verify-password").val().trim();
        if(!current_password || !new_password || !verify_password){
            alertify.error("You must complete all field.");
            return;
        }
        if(new_password != verify_password){
            alertify.error("New password and verify password are differents");
            return;
        }
        request=patchFabberPass(username,current_password,new_password);
        request.done(function(data,status,jqxhr){
            alertify.success("Password changed successfully");
        });
        request.fail(function(data,status,jqxhr){
            alertify.error("Password was not changed");
        });
    }

    function prepareUpload(event){
        files = event.target.files;
        var formData = new FormData();
        formData.append("file", files[0]);
        $("#status_upload_profile_photo").html("Uploading....");        
        request=$.ajax({
          url: "./api/v1/photo/"+username,
          type: "PUT",
          data: formData,
          processData: false,  // tell jQuery not to process the data
          contentType: false   // tell jQuery not to set contentType
        });
        request.done(function(data,status,jqxhr){
            $("#status_upload_profile_photo").html("Uploaded.");        
            $(".photo-profile").attr("src","../"+photo+"?lastmod="+new Date().toString());
        })
    }


 