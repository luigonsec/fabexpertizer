/* 
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */



$(document).ready(function(){
    
    $("#password-confirm").on("focusout",function(){
        if($("#password").val()!=$("#password-confirm").val()){
            $(".pass").addClass("has-error");
            $("#password-error").removeClass("hidden");
        }else if($("#password").val()==$("#password-confirm").val()){
            $("#password-error").addClass("hidden");
            $(".pass").removeClass("has-error");
        }
    });
    $("#username").on("focusout",function(){

        var request=getFabber($("#username").val());
        request.done(function(data, textStatus, jqXHR){
            if($("#username").val()==data.username){
                $("#username-error").removeClass("hidden");
                $(".user").addClass("has-error");
                alertify.error("Sorry, this username already exist.");
            }
        });
        request.fail(function(jqXHR, textStatus, errorThrown){
            $("#username-error").addClass("hidden");
            $(".user").removeClass("has-error");
            if ($("#username").val()!=""){
                alertify.success("You can use this username.");
            }
        });

    });
    $("#password").on("focusout",function(){
        if($("#password").val()==$("#password-confirm").val()){
            $(".error-p").remove();
        }
    });
    $("#signup").on("click",function(){
        if($("#password").val()=="" || $("#name").val()=="" || $("#surname").val()=="" || $("#email").val()==""){
            alertify.error("All fields are required");
        }else{
            
            if ($('#username-error').hasClass('hidden') && $('#password-error').hasClass('hidden')){
                request=postFabber($("#name").val(), $("#surname").val(),$("#username").val(), $("#email").val(), $("#password").val());
                request.done(function(data, textStatus, jqXHR){
                    alertify.success("Congratulation, now you are a fabber!!!");
                    window.location.replace("./index.html");
                });
                request.fail(function(jqXHR, textStatus, errorThrown){
                    alertify.error("We're sorry, you were unable to be signup");
                });
            } else{
                alertify.error("There are any errors, check the fields in red");
            }
        }
    });
    
});