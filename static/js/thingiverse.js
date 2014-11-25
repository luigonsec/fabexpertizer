/* 
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
var clientID="bb4056d993e5c7cbe200";
var clientSecret="8d3289e1a5bc0482779b726ee00f552d";         
var code=null;
var dat=Array();
var accessToken=null;
var tokenType=null;
$(document).ready(function(){
        code=getURLParameter('code');
        dat['code']=code;
        dat['client_id']=clientID;
        dat['client_secret']=clientSecret;
        var request=$.ajax({
                type: "POST",
                url: "https://www.thingiverse.com/login/oauth/access_token",
                data: dat,
                success:function(data, textStatus, jqXHR ){
                   accessToken=getURLParameter("access_token");
                   tokenType=getURLParameter("token_type");
                   $("#things").removeClass("hidden");
                   alert("your access token is: "+accessToken);
                },
                error:function(jqXHR, textStatus, errorThrown ){
                    alert( "Error, can't get token. Error thrown: "+errorThrown+" . Text status : "+textStatus );
                }
                
        });
        $("#getThings").on('click',function(){
            var request=$.ajax({
                type: "GET",
                url: "https://api.thingiverse.com/users/TeamTeamUSA/things/",
                beforeSend: function (xhr) {
                    xhr.setRequestHeader('Authorization', tokentType+ " " + accessToken);
                },
                success:function(data, textStatus, jqXHR ){
                   $("TeamHeader").before("<p>"+data+"</p>");
                },
                error:function(jqXHR, textStatus, errorThrown ){
                    alert( "Error, can't get things. Error thrown: "+errorThrown+" . Text status : "+textStatus );
                }
            });
            
        });
        
});

function getURLParameter(name) {
  return decodeURIComponent((new RegExp('[?|&]' + name + '=' + '([^&;]+?)(&|#|;|$)').exec(location.search)||[,""])[1].replace(/\+/g, '%20'))||null;
}