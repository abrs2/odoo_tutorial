/* Created by jankoatwarpspeed.com */
'use strict';

odoo.define('pao_fans_automation.website_form', function (require) {
    require('web.dom_ready');
    var ajax = require('web.ajax');

    var country = $('#application_legalEntityCountry');
    var state = $('#application_legalEntityState');
    var city = $('#application_legalEntityCity');
    
    ajax.jsonRpc('/get_globalgap_countries', 'call', {}).then(function (data) {
        console.log(data);
        var option = '';
        for (var i = 0; i < data.length; i++) {
            if (data[i].name == "México") {
                option += '<option selected="selected" value="' + data[i].id + '">' + data[i].name + '</option>';
                loaded=true;
            } else {
                option += '<option value="' + data[i].id + '">' + data[i].name + '</option>';
            }
        }
        $('#application_legalEntityCountry').empty().append(option);
        $('#application_legalEntityState').empty();
        $('#application_legalEntityCity').empty();
    });
    

    var _onChangeCountry = function (e) {
        selectedCountry = parseInt($('#application_legalEntityCountry').val());
        ajax.jsonRpc('/get_globalgap_states', 'call', {'country_id':selectedCountry}).then(function (data) {
            console.log(data);
            console.log(selectedCountry);
            var option = '';
            for (var i = 0; i < data.length; i++) {
                
                option += '<option value="' + data[i].id + '">' + data[i].name + '</option>';
           
            }
            $('#application_legalEntityState').empty().append(option);
            $('#application_legalEntityCity').empty();
        });
    }

    country.change(_onChangeCountry);

    var _onChangeState = function (e) {
        selectedState = parseInt($('#application_legalEntityState').val());
        ajax.jsonRpc('/get_globalgap_cities', 'call', {'state_id':selectedState}).then(function (data) {
            console.log(data);
            console.log(selectedState);
            var option = '';
            for (var i = 0; i < data.length; i++) {
                
                option += '<option value="' + data[i].id + '">' + data[i].name + '</option>';
           
            }
            $('#application_legalEntityCity').empty().append(option);
            
        });
    }

    state.change(_onChangeState);
    /*
    -------------------
    var _onSelectCountry = function (e) {
        ajax.jsonRpc('/get_globalgap_countries', 'call', {}).then(function (data) {
            console.log(data);
            var option = '';
            for (var i = 0; i < data.length; i++) {
                if (data[i].name == "México" && !loaded) {
                    option += '<option selected="selected" value="' + data[i].id + '">' + data[i].name + '</option>';
                    loaded=true;
                } else {
                    option += '<option value="' + data[i].id + '">' + data[i].name + '</option>';
                }
            }
            $('#application_legalEntityCountry').empty().append(option);
        });
    }

    country.click(_onSelectCountry);
    */
  

    /*$(document).ready(function () {
        $('#application_legalEntityCountry').on('load', function (e) {

            ajax.jsonRpc('/get_globalgap_countries', 'call', {}).then(function (data) {
                console.log(data);
                var option = '';
                for (var i = 0; i < data.length; i++) {
                    option += '<option value="' + data[i].id + '">' + data[i].name + '</option>';
                }
                $('#application_legalEntityCountry').append(option);
            });

        });
    });*/
});