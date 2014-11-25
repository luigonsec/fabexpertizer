/* 
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */



$(document).ready(function(){

    $("#signin").on("click",function(){
        login();
    });
    $("form").keypress(function(key){
        if(key.which==13){
            login();
        }
    });
    
});

function login (){
    var fabber='{"username":"'+$("#username").val()+'", "password":"'+$("#password").val()+'"}';
    request=$.ajax({
                   url: "./login",
                   type: "POST",
                   data: fabber,
                   contentType: "application/json"
                   });
    request.done(function(data, textStatus, jqXHR){
                 window.location.href = "./blog";
                 });
    request.fail(function(jqXHR, textStatus, errorThrown){
                 $("#login-error").removeClass("hidden");
                 alertify.error("Sorry, check your username and password");
                 });
}