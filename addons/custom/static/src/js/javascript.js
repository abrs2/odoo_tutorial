odoo.define('custom.products',['web.ajax'], function (require){
    "use strict";

    var ajax= require('web.ajax');

    $(document).ready(function(){
        var container = document.getElementById("products");

        if (container){
            container.innerHTML="";
            container.innerHTML="<div class='col text-center'>Cargando</div>";

            ajax.jsonRpc('/get_products','call',{}).then(function(data){
                container.innerHTML="";
                console.log(data);
                for(var i=0; i<data.length; i++){
                    container.innerHTML += '<div class="col-12 col-sm-6 col-md-4 col-lg-4 mb-3">\
                                                <h6 class="text-center mt-3 pb-1">'+ data[i].name + '</h6>\
                                                <h6 class="text-center mt-3 pb-1">'+ data[i].list_price + '</h6>\
                                            </div>\
                                            <br>';
                }
            });
        }
    });

});