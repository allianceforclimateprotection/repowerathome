/*jslint maxerr: 1000, white: true, browser: true, devel: true, rhino: true, onevar: false, undef: true, nomen: true, eqeqeq: true, plusplus: true, bitwise: true, regexp: true, newcap: true, immed: true, sub: true */
/*global $: false, RAH: false, FB: false, WebFont: false, jQuery: false, window: false, google: false, require: false, define: false */
require(["libs/jquery.validation", "libs/jquery.ui", "mods/search"],
    function (validation, ui, search) {
        var form = $('.search_widget');
        $('#search_widget_input').autocomplete({
            source: function (req, res) {
                $.ajax({
                    url: form.attr('action'),
                    dataType: 'json',
                    data: {
                        search: req.term,
                        format: 'json',
                        fields: 'id,place_name,location__zipcode'
                    },
                    success: function (data) {
                        res($.map(data, function (item) {
                            return {
                                label: item.location__zipcode,
                                value: item.id
                            };
                        }));
                    }
                });
            },
            minLength: 2
        }).data('autocomplete')._renderItem = function (ul, item) {
            return $('<li/>', {
                id: item.value,
                text: item.label
            }).appendTo(ul);
        };
        $("#house_party_form").validate({ rules: { phone_number: { required: true }}});
        $('#house_party_link').click(function () { 
            $('#house_party_dialog').dialog('open'); 
            return false; 
        });
        $('#house_party_dialog').dialog({
            title: 'Energy meeting contact', 
            modal: true, 
            resizable: false, 
            draggable: false, 
            autoOpen: false, 
            buttons: { "Give me a call": function () { 
                $('#house_party_form').submit(); 
            }}
        });
    });
