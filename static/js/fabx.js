/* 
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

    var source=null;
    var front=null;
    var username=null;
    var top=null;
    var left=null;
// Fabx code
$(document).ready(function(){
        $('#li_fabex').attr("class","active");

        $('#source').on('change',function(){
            source=this.files[0];
        });

        username = getCookie("username");
        $('#btn-top').on('change',function(){
            top=this.files[0];
        });
        $('#btn-left').on('change',function(){
            left=this.files[0];
        });
        $('#btn-front').on('change',function(){
            front=this.files[0];
        });
        //Post Fabex
        $('#send').on('click',function(){
            var fabex=createFabex();
            request=postFabex(fabex);
            request.done(function(data, textStatus, jqXHR){
                alertify.success("Fabex create.");
                uploadfiles(data);
                setTimeout($(location).attr('href',location.origin+'/blog/'+Number(data._id)),2000);
            });
            request.fail(function(jqXHR, textStatus, errorThrown){
                alertify.alert(jqXHR+","+textStatus);
            });
        });
        
        // Wizard code
        $('#next').on('click',function (){
            if($('#selected-machine').val()!="" && $('#form').attr('page')==1){
                $('#form').attr('page',parseInt($('#form').attr('page'))+1);
                $('#next').addClass('hidden');
                $('#general').addClass('hidden');
                $('#machine').removeClass('hidden');
            }else if ($('#form').attr('page')==0){
                $('#form').attr('page',parseInt($('#form').attr('page'))+1);
                $('#previous').removeClass('hidden');
                $('#photo-form').addClass('hidden');
                $('#general').removeClass('hidden');
            }else if($('#selected-machine').val()==""){
                alertify.error("Please, select machine");
            }
        });
        
        $('#previous').on('click',function (){
            if($('#form').attr('page')==1){
                $('#form').attr('page',parseInt($('#form').attr('page'))-1);
                $('#previous').addClass('hidden');
                $('#general').addClass('hidden');
                $('#photo-form').removeClass('hidden');
            }else if($('#form').attr('page')==2){
                $('#form').attr('page',parseInt($('#form').attr('page'))-1);
                $('#next').removeClass('hidden');
                $('#machine').addClass('hidden');
                $('#general').removeClass('hidden');
            }
        });
               
        $('#selected-machine').on('change',function (){
            if($('#selected-machine').val()!="" ){
                loadMachineForm();
            }else{
                $('#machine-properties').children().remove();
            }
        });
        $('#machine-properties').on('change','#material',function (){
            loadThickness();
        });
        //End wizard code

    if($("#author").data("admin")=="1"){    
        loadAuthor();
    }
    loadFablabs(username);
    loadMachines();
    preparePhotos();
    $("#author").on("change",function(){
        loadFablabs($("#author").val());
    })

});


//Machine load
function loadMachines(){
    var requestMachines=getMachines();
    requestMachines.done(function(data, textStatus, jqXHR){
        for(var i=0;i<data.length;i++){
            var option='<option value="'+data[i].name+'">'+data[i].name+'</option>';
            $('#selected-machine').append(option);
        }
    });
}

function loadFablabs(val){
    if(!val){
        var requestFablabs=getFabberFablabs(username);
    }else{
        var requestFablabs=getFabberFablabs(val);
    }
    requestFablabs.done(function(data, textStatus, jqXHR){
        $('#selected-fablab').empty();
        for(var i=0;i<data.length;i++){
            var option='<option value="'+data[i].fablab+'">'+data[i].name+'</option>';
            $('#selected-fablab').append(option);
        }
    });
    requestFablabs.fail(function(data,textStatus,jqxhr){
        console.log(data.responseText);
    });
}

//Thickness load
function loadThickness(){

        if($('#material').val()!=''){
            var request=getMaterial($('#material').val());
            request.done(function(data, textStatus, jqXHR){
                material=data;
                if (typeof material.thicknesses != 'undefined'){
                    var material={values:material.thicknesses,type:'select',name:'Thicknes'};
                    var input=getPropertyCode(material);
                    $('#material').before(input);
                }else{
                    $('.material-thickness').remove();
                }
            });
        }else{
            $('#thickness').addClass('hidden');
            $('.thickness-option').remove();
        }

}
//Material load
function loadMaterials(){
    if(typeof $('#material')!='undefined'){
        var requestMaterials=getMaterials();
        requestMaterials.done(function(data, textStatus, jqXHR){
            for(var i=0;i<data.length;i++){
                if($('#selected-machine').val()==data.machine){
                    var option='<option class="material-option"value="'+data[i].name+'">'+data[i].name+'</option>';
                    $('#material').append(option);
                }
            }
        });
        requestMaterials.fail(function(jqXHR, textStatus, errorThrown){
            alert("No se han cargado los materiales");
        });
    }
}

//Author load
function loadAuthor(){
    var requestFabber=getFablabMembers(getCookie("username"));
    requestFabber.done(function(data, textStatus, jqXHR){
        for(var i=0;i<data.length;i++){
                var option='<option value="'+data[i]+'">'+data[i]+'</option>';
                $('#author').append(option);
        }
    });
    requestFabber.fail(function(data, textStatus, jqXHR){
        console.log(data.responseText);
    });
}


// Get data from form and build fabex object, to do
function createFabex(){
    var fabex=null
    var blogVar=($('#blog').val()=='on');
    var fabexProperties=getProperties();
    fabex={title:$('#title').val(),description:$('#description').val(),author:$('#author').val(),blog:blogVar,fablab:$('#selected-fablab').val(),machine:$('#selected-machine').val(),properties:fabexProperties,front:$('#btn-front').attr('src'),left:$('#btn-left').attr('src'),top:$('#btn-top').attr('src')};
    return fabex;
}
function getProperties(){
    var properties = new Array();
    var propertiesDiv=$('#machine-properties').children();
    var div = propertiesDiv.first('div');
    for(var i=0;i<propertiesDiv.length;i++){
        var property={name:div.find('.property').attr('id'),value:div.find('.property').val()};
        properties.push(property);
        div=div.next();
    }

    
    
    return properties
}
// Revisar
function uploadfiles(data){
    //Upload files

    if ($('#source').attr('src')!=""){
        var sourceRequest=postSource(source,data._id);
    }

}

function preparePhotos(){
    // Photos code
    if($('#photo-canvas')!=null){
        var video = document.getElementById('video');
        var canvas = document.getElementById('photo-canvas');
        var ctx = canvas.getContext('2d');
        if (hasUserMedia()) {
            console.log("Ok, the browser support UserMedia");
        } else {
            alert('Mala suerte: getUserMedia() no está soportado en tu navegador. ¿Conoces Chrome?');
        }
        //Comprueba los diferentes motores que dan soporte
        function hasUserMedia() {
            return navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia;
        }
        
        /////////////////////////////////
        /////////////////////////////////
        
        //Similar a los prefijos de CSS, usamos variables para contener los posibles
        //objetos usados en cada navegador
        
        window.URL = window.URL || window.webkitURL;
        
        navigator.getUserMedia  = navigator.getUserMedia || navigator.webkitGetUserMedia ||
        navigator.mozGetUserMedia || navigator.msGetUserMedia;
        
        //var video = document.querySelector('video');
        
        //Comprobamos si existe getUserMedia y si no lanzamos un error
        if (navigator.getUserMedia) {
            navigator.getUserMedia({video: true}, success, error);
            //Llámamos getUserMedia, pedimos acceso a vídeo. Si tenemos éxito llamamos una función y si no, lanzamos un error.
        } else {
            error();
        }
        
        //Si soportamos getUserMedia y damos permiso, nuestro tag de video mostrará el stream que recogemos.
        function success(stream) {
            video.src = window.URL.createObjectURL(stream);
        }
        
        //Nuestro error lanza un simple mensaje alert.
        function error(e) {
            alert("Something was wrong");
        }
        
        function getImage(){
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            ctx.drawImage(video, 0, 0);
            return canvas.toDataURL();
        }
        
        $('#btn-front').on('click', function(){
                           $(this).attr("src", getImage());
                           });
        
        $('#btn-top').on('click', function(){
                         $(this).attr("src", getImage());
                         });
        
        $('#btn-left').on('click', function(){
                          $(this).attr("src", getImage());
                          });
    }
    
    // End photos code

}

function loadMachineForm(){
    var requestMachine =getMachine($('#selected-machine').val());
    requestMachine.done(function(data, textStatus, jqXHR){
        var elementOpen='<div class="form-group machine-item "><div class="col-sm-offset-2 col-sm-8">';
        var elementClose='</div></div>';
        $('#machine-properties').children().remove();
        for(var i=0;i<data.properties.length;i++){
            var div =elementOpen+getPropertyCode(data.properties[i])+elementClose;
            $('#machine-properties').append(div);
        }
        $('[data-toggle="tooltip"]').tooltip({trigger: 'hover'});
    });
}

function getPropertyCode(property){
    var input=null;
    switch(property.type){
        case 'text':
            input='<input id="'+property.name+'" class="form-control property" type="text" data-toggle="tooltip" data-placement="right" title="'+property.description+'" placeholder="'+property.name+'">';
            break;
        case 'checkbox':
            input='<label ><input id="'+property.name+'" class="property" type="checkbox" data-toggle="tooltip" data-placement="right" title="'+property.description+'">'+property.name+'</label>';
            break;
        case 'select':
            input='<select id="'+property.name+'" class="form-control property" data-toggle="tooltip" data-placement="right" title="'+property.description+'"><option value="" selected="selected">Select '+property.name.toLowerCase()+'</option>';
            for(var i=0;i<property.values.length;i++){
                input=input+'<option value="'+property.values[i]+'" selected="selected">'+property.values[i]+'</option>';
            }
            break;
        case 'date':
            input='<input id="'+property.name+'" class="form-control property" data-toggle="tooltip" data-placement="right" title="'+property.description+'" type="date">';
            break;
    }
    return input;
}



