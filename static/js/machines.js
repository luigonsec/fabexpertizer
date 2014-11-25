$(document).ready(function(){

    $("#li_admin").attr("class","active");
    $('#option-profile-machines').attr("class","active");

    $('#addProperty').on('click',function(){
        newProperty();
        $('#fieltset').removeClass('hidden');
    });
    $('#selected-machine').on('change',function(){
        $('#properties').children().remove();
        loadForm();
        
    });
    $('#properties').on('change','.property-select',function(){
        var propertyDiv=$(this).parent().parent().parent();
        showPropertyExample(propertyDiv, $(this).val());
    });
    $('#submit').on('click',function(){
        var create =$('#create').hasClass('active');
        var modify =$('#modify').hasClass('active');
        var del =$('#delete').hasClass('checked');
        if($('#create').hasClass('active')){
            var request = createMachine();
            request.done(function(data, textStatus, jqXHR){
                alertify.success("Create.");
            });
            
        }else if($('#modify').hasClass('active')){
            var request = modifyMachine();
            request.done(function(data, textStatus, jqXHR){
                alertify.success("Modify");
            });
            request.fail(function(jqXHR, textStatus,  errorThrown){
                alertify.error(errorThrown);
            });
        }else if($('#delete').hasClass('active')){
            var request = deleteMachine();
            request.done(function(data, textStatus, jqXHR){
                alertify.success("Delete.");
            });
            
        }
    });
    $('.switch').on('click',function(){
        var form =$(this).attr('id');
        showForm(form);
        $('#properties').children().remove();
    });
    $('#properties').on('click','.deleteProperty',function(){
        $(this).parent().parent().parent().remove();
    });

                  
});
function showForm(form){
    if (form=='create'){
        $('.input').prop('disabled',false);
        $('.input').val('');
        $('#selected-machine').addClass('hidden');
        $('#name').removeClass('hidden');
        $('#fieltset').addClass('hidden');
        
    }else if(form=='modify'){
        $('.input').prop('disabled',false);
        $('.input').val('');
        $('#name').addClass('hidden');
        $('#selected-machine').removeClass('hidden');
        loadMachines()
        $('#fieltset').removeClass('hidden');
    }else if(form=='delete'){
        $('.input').prop('disabled',true);
        $('.input').val('');
        $('#name').addClass('hidden');
        $('#selected-machine').removeClass('hidden');
        loadMachines()
        $('#fieltset').removeClass('hidden');
    }
    
}
function newProperty(){
    var property =$('#machine_property_template').find('.propertyDiv').clone();
    //'<div id="property'+$('#properties').children().length+'" class="propertyDiv col-sm-8 row" ><input type="button" class="btn btn-danger deleteProperty" value="-"><input id="name'+$('#properties').children().length+'" type="text" placeholder="Property name" class="form-control col-sm-4 name input" ><textarea id="description'+$('#properties').children().length+'" placeholder="Property description" class="form-control description input"></textarea><select class="form-control col-sm-4 property-select type input" id="type'+$('#properties').children().length+'"><option value="" selected="selected">Select property type</option><option value="text" >Text</option><option value="checkbox" >Boolean</option><option value="select" >Select</option><option value="date" >Date</option></select></div>';
    $('#properties').append(property);

}

function showPropertyExample(div, type){
    var input=null;
    div.children('.example').remove();
    switch(type){
        case 'text':
            input=$('#form_item_template').find('.text').clone();
            break;
        case 'checkbox':
            input=$('#form_item_template').find('.checkbox').clone();
            break;
        case 'select':
            input=$('#form_item_template').find('.select').clone();
            break;
        case 'date':
            input=$('#form_item_template').find('.date').clone();
            break;
    }
    div.append(input);
}

function getMachineObject(form){
    var propertiesArray = new Array();
    var propertiesDiv=$('#properties').children();
    var div = propertiesDiv.first('div');
    var property=null
    for(var i=0;i<propertiesDiv.length;i++){
        if(div.find('.type').val()=='select'){
            property={name:div.find('.name').val(),description:div.find('.description').val(),type:div.find('.type').val(),values:div.find('.values').val().split(',')};
        }else{
            property={name:div.find('.name').val(),description:div.find('.description').val(),type:div.find('.type').val()};
        }
        propertiesArray.push(property);
        div=div.next();
    }
    var machineName=null;
    if (form=='create'){
        machineName=$('#name').val();
    }else{
        machineName=$('#selected-machine').val();
    }
    
    var machine={name:machineName,model:$('#model').val(),description:$('#description').val(),properties:propertiesArray};
    return machine;
}

function createMachine(){
    var machine=getMachineObject();
    return postMachine(machine);
}

function modifyMachine(){
    var machine=getMachineObject();
    return patchMachine(machine);
}
function deleteMachine(){
    var machine=getMachineObject();
    return deleteMachine(machine.name);
}


function loadMachines(){
    var requestMachines=getMachines();
    requestMachines.done(function(data, textStatus, jqXHR){
        $('#selected-machine').children().remove();
        var option='<option value="">Select machine</option>';
        $('#selected-machine').append(option);
        for(var i=0;i<data.length;i++){
            option='<option value="'+data[i].name+'">'+data[i].name+'</option>';
            $('#selected-machine').append(option);
        }
    });
}

function loadForm(){
    if($('#selected-machine').val()!=''){
        var machine =getMachine($('#selected-machine').val());
        machine.done(function(data, textStatus, jqXHR){
            $('#model').val(data.model);
            $('#description').val(data.description);
            for(var i=0;i<data.properties.length;i++){
                var property =$('#machine_property_template').find('.propertyDiv').clone();
                     '<div id="property'+i+'" class="propertyDiv col-sm-8 row" >';
                if($('#delete').hasClass('active')){
                     property.find('.deleteProperty').addClass('hidden');
                    //=property+'<input type="button" class="btn btn-danger deleteProperty" value="-">';
                }
                property.find('.name').val(data.properties[i].name);
                property.find('.description').val(data.properties[i].description);
                //=property+'<input id="name'+i+'" type="text" placeholder="Property name" class="form-control col-sm-4 name input" value="'+data.properties[i].name+'" ><textarea id="description'+i+'" placeholder="Property description" class="form-control description input" >'+data.properties[i].description+'</textarea>';
                switch(data.properties[i].type){
                     case 'text':
                        property.find('.property-select option[value="text"]').attr('selected', 'selected');
                        property.append($('#form_item_template').find('.text').clone());
                        //=property+'<select class="form-control col-sm-4 property-select type input" id="type'+i+'"><option value="" >Select property type</option><option selected value="text" >Text</option><option value="checkbox" >Boolean</option><option value="select" >Select</option><option value="date" >Date</option></select>';
                        break;
                     case 'checkbox':
                        property.find('.property-select option[value="checkbox"]').attr('selected', 'selected');
                        property.append($('#form_item_template').find('.checkbox').clone());
                     //=property+'<select value="checkbox" class="form-control col-sm-4 property-select type input" id="type'+i+'"><option value="" >Select property type</option><option value="text" >Text</option><option selected value="checkbox" >Boolean</option><option value="select" >Select</option><option value="date" >Date</option></select>';
                        break;
                     case 'select':
                        property.find('.property-select option[value="select"]').attr('selected', 'selected');
                        property.append($('#form_item_template').find('.select').clone());
                        var values=property.find('.values');
                        //=property+'<select value="select" class="form-control col-sm-4 property-select type input" id="type'+i+'"><option value="" selected="selected">Select property type</option><option value="text" >Text</option><option value="checkbox" >Boolean</option><option selected value="select" >Select</option><option value="date" >Date</option></select>';
                        //property=property+'<textarea id="values'+i+'" placeholder="Property values sparated by coma" class="form-control values example input">';
                        var string='';
                        for(var j=0;j<data.properties[i].values.length;j++){
                            if(j<data.properties[i].values.length-1){
                                string=string+data.properties[i].values[j]+',';
                            }else{
                                string=string+data.properties[i].values[j];
                            }
                        }
                        values.val(string);
                        //property=property+'</textarea>';
                        break;
                     case 'date':
                        property.find('.property-select option[value="date"]').attr('selected', 'selected');
                        //property=property+'<select value="date" class="form-control col-sm-4 property-select type input" id="type'+i+'"><option value="" selected="selected">Select property type</option><option value="text" >Text</option><option value="checkbox" >Boolean</option><option value="select" >Select</option><option selected value="date" >Date</option></select>';
                        break;
                     }
                //property=property+'</div>';
                $('#properties').append(property);
            }
            if($('#delete').hasClass('active')){
                $('#properties').find('.form-control').prop('disabled',true);
            }
        });
    }else{
        $('.input').val('');
    }
    
}




