/*jslint maxerr: 1000, white: true, browser: true, devel: true, rhino: true, onevar: false, undef: true, nomen: true, eqeqeq: true, plusplus: true, bitwise: true, regexp: true, newcap: true, immed: true, sub: true */
/*global $: false, FB: false, WebFont: false, jQuery: false, window: false, google: false, require: false, define: false */
define(["libs/jquery.ui", "mods/messages", "libs/jquery.validation"], 
    function (ui, messages, validate) {
        return {
            link_setup: function () {
                $(".commit_action").click(function () {
                    var elem = $(this);
                    elem.siblings("span.commit_tick")
                        .toggleClass("ui-icon-triangle-1-e")
                        .toggleClass("ui-icon-triangle-1-s");
                    $("td .commit_list_ul_" + elem.attr("id").split("__")[1]).toggle();
                });
                $(".commit_list_ul li").hover(function () {
                    $(this).children(".commit_user_list_edit_link").toggle();
                });
            },
            card_setup: function () {
                $("#commitment_card_dialog").remove();
                $('body').append('<div id="commitment_card_dialog"></div>');
                $("#commitment_card_dialog").dialog({
                    modal: true,
                    buttons: {
                        "Save and close": function () { 
                            $("#commitment_card_form").ajaxSubmit({
                                success: function (messages_html) {
                                    $("#commitment_card_dialog").dialog("close");
                                    messages.add_message(messages_html);
                                    $("#commitments_show_table").load('/commitments/ #commitments_show_table table', function () {
                                        this.link_setup();
                                    });
                                }
                            });
                        }
                    },
                    autoOpen: false,
                    width: 781
                });
                
                // Attach functionality commitment card links
                $(".commitment_card_open").click(function () {
                    var href = $(this).attr('href');
                    
                    $("#commitment_card_dialog").load(href, function () {
                        this.form_setup(href);
                        $("#commitment_card_dialog").dialog("open");
                    });
                    return false;
                });
            },
            form_setup: function (action) {
                $("#commitment_card_form .commit_card_choice input").live("click", function () {
                    var id = $(this).attr("id");
                    var index = id.substr(id.length - 1, 1);
                    var other_index = (index === "1") ? "0" : "1";
                    var field_name = id.substr(0, id.length - 1);
                    $("#" + field_name + other_index).attr("checked", false);
                });
                
                $("#commitment_card_form").validate({
                    rules: {
                        zipcode:    { required: false, minlength: 5, digits: true },
                        email:      { required: false, email: true },
                        first_name: { required: true, minlength: 2 }
                    }
                });
                
                $("#commitment_card_form").attr("action", action);
                
                $("#commitment_card_select_form #id_form_name").change(function () {
                    var load_url = action + '?form_name=' + $(this).val();
                    $("#commitment_card_action_table").load(load_url + ' #commitment_card_action_table table');
                    $("#commitment_card_form").attr("action", load_url);
                });
            }
        };
    });
